#!/usr/bin/env python3
"""
verify_index.py — Verify the SurvivalAI FTS5 search index.

Checks database integrity, validates article coverage, tests search
functionality, and reports any issues.

Usage:
    python3 verify_index.py [--db ./search/knowledge.db] [--docs-dir ./docs] [--fix]

This script is PRIVATE — not included in the public repo or shipped on the drive.
"""

import sqlite3
import os
import sys
import hashlib
import argparse
from pathlib import Path


# Expected categories and minimum article counts
EXPECTED_CATEGORIES = {
    'medicine': 15,
    'water': 8,
    'food': 12,
    'shelter': 8,
    'fire': 7,
    'navigation': 7,
    'energy': 7,
    'communications': 7,
    'agriculture': 11,
    'mechanical': 8,
    'chemistry': 7,
    'community': 7,
    'textiles': 6,
    'references': 6,
}

TOTAL_EXPECTED = sum(EXPECTED_CATEGORIES.values())  # 116 minimum (excluding wound-care + purification already in repo)

# Queries that MUST return results (critical content verification)
REQUIRED_QUERIES = [
    ('wound care bleeding', 'medicine'),
    ('water purification boiling', 'water'),
    ('CPR chest compressions', 'medicine'),
    ('fire starting friction', 'fire'),
    ('edible plants identification', 'food'),
    ('shelter emergency debris', 'shelter'),
    ('compass navigation north', 'navigation'),
    ('solar panel battery', 'energy'),
    ('radio frequency emergency', 'communications'),
    ('soil compost garden', 'agriculture'),
    ('engine repair carburetor', 'mechanical'),
    ('soap making lye', 'chemistry'),
    ('group leadership conflict', 'community'),
    ('sewing patching repair', 'textiles'),
    ('knot bowline hitch', 'references'),
    ('antibiotic dosage infection', 'medicine'),
    ('water bleach chlorine drops', 'water'),
    ('bleeding tourniquet', 'medicine'),
    ('fracture splint broken bone', 'medicine'),
    ('burn treatment blister', 'medicine'),
]


def compute_file_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


class Verifier:
    def __init__(self, db_path, docs_dir=None):
        self.db_path = db_path
        self.docs_dir = docs_dir
        self.errors = []
        self.warnings = []
        self.passed = 0
        
    def error(self, msg):
        self.errors.append(msg)
        print(f"  FAIL: {msg}")
    
    def warn(self, msg):
        self.warnings.append(msg)
        print(f"  WARN: {msg}")
    
    def ok(self, msg):
        self.passed += 1
        print(f"  OK:   {msg}")
    
    def check_db_exists(self):
        print("\n[1] Database file check")
        if not os.path.exists(self.db_path):
            self.error(f"Database not found: {self.db_path}")
            return False
        
        size = os.path.getsize(self.db_path)
        if size < 1024:
            self.error(f"Database suspiciously small: {size} bytes")
            return False
        
        self.ok(f"Database exists: {size / 1024:.1f} KB")
        return True
    
    def check_integrity(self):
        print("\n[2] SQLite integrity check")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        try:
            cur.execute("PRAGMA integrity_check")
            result = cur.fetchone()[0]
            if result == 'ok':
                self.ok("PRAGMA integrity_check passed")
            else:
                self.error(f"Integrity check failed: {result}")
        except Exception as e:
            self.error(f"Integrity check error: {e}")
        
        conn.close()
    
    def check_tables(self):
        print("\n[3] Table structure check")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        required_tables = ['articles', 'search_index', 'sections', 'build_info']
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing = {row[0] for row in cur.fetchall()}
        
        for table in required_tables:
            if table in existing:
                self.ok(f"Table '{table}' exists")
            else:
                # FTS5 tables show up differently
                if table == 'search_index':
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'search_index%'")
                    fts_tables = cur.fetchall()
                    if fts_tables:
                        self.ok(f"FTS5 table 'search_index' exists ({len(fts_tables)} internal tables)")
                    else:
                        self.error(f"FTS5 table 'search_index' not found")
                else:
                    self.error(f"Table '{table}' missing")
        
        conn.close()
    
    def check_article_counts(self):
        print("\n[4] Article count check")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute("SELECT count(*) FROM articles")
        total = cur.fetchone()[0]
        
        if total >= TOTAL_EXPECTED - 5:  # Allow small variance
            self.ok(f"Total articles: {total} (expected ~{TOTAL_EXPECTED})")
        elif total > 0:
            self.warn(f"Total articles: {total} (expected ~{TOTAL_EXPECTED} — {TOTAL_EXPECTED - total} may be missing)")
        else:
            self.error(f"No articles in database!")
        
        # Check per category
        cur.execute("SELECT category, count(*) FROM articles GROUP BY category ORDER BY category")
        categories = dict(cur.fetchall())
        
        for cat, expected in sorted(EXPECTED_CATEGORIES.items()):
            actual = categories.get(cat, 0)
            if actual >= expected:
                self.ok(f"  {cat}: {actual} articles (expected {expected})")
            elif actual > 0:
                self.warn(f"  {cat}: {actual} articles (expected {expected} — missing {expected - actual})")
            else:
                self.error(f"  {cat}: 0 articles (expected {expected})")
        
        # Check for unexpected categories
        for cat in categories:
            if cat not in EXPECTED_CATEGORIES:
                self.warn(f"  Unexpected category: '{cat}' ({categories[cat]} articles)")
        
        conn.close()
    
    def check_fts_search(self):
        print("\n[5] FTS5 search functionality check")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        for query, expected_cat in REQUIRED_QUERIES:
            try:
                cur.execute('''
                    SELECT s.category, s.title, rank
                    FROM search_index s
                    WHERE search_index MATCH ?
                    ORDER BY rank
                    LIMIT 5
                ''', (query,))
                results = cur.fetchall()
                
                if not results:
                    self.error(f"Query '{query}' returned 0 results")
                else:
                    # Check if expected category is in results
                    result_cats = [r[0] for r in results]
                    if expected_cat in result_cats:
                        self.ok(f"'{query}' → {len(results)} results (top: {results[0][1]})")
                    else:
                        self.warn(f"'{query}' → {len(results)} results but expected category '{expected_cat}' not in top 5")
            except Exception as e:
                self.error(f"Query '{query}' failed: {e}")
        
        conn.close()
    
    def check_sections(self):
        print("\n[6] Section coverage check")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute("SELECT count(*) FROM sections")
        sec_count = cur.fetchone()[0]
        
        cur.execute("SELECT count(*) FROM articles")
        art_count = cur.fetchone()[0]
        
        if sec_count > 0:
            avg = sec_count / max(art_count, 1)
            self.ok(f"Total sections: {sec_count} (avg {avg:.1f} per article)")
        else:
            self.error("No sections in database")
        
        # Check for articles with no sections
        cur.execute('''
            SELECT a.category, a.filename FROM articles a
            LEFT JOIN sections s ON a.id = s.article_id
            WHERE s.id IS NULL
        ''')
        orphans = cur.fetchall()
        if orphans:
            for cat, fname in orphans:
                self.warn(f"Article with no sections: [{cat}] {fname}")
        else:
            self.ok("All articles have at least one section")
        
        # Check for empty content
        cur.execute("SELECT count(*) FROM sections WHERE content = '' OR content IS NULL")
        empty = cur.fetchone()[0]
        if empty > 0:
            self.warn(f"{empty} sections have empty content")
        else:
            self.ok("No empty sections")
        
        conn.close()
    
    def check_file_hashes(self):
        """Compare stored hashes with actual files to detect drift."""
        if not self.docs_dir:
            return
        
        print("\n[7] File hash verification (index vs source files)")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute("SELECT category, filename, file_hash FROM articles")
        rows = cur.fetchall()
        
        docs_path = Path(self.docs_dir)
        checked = 0
        mismatches = 0
        missing = 0
        
        for cat, fname, stored_hash in rows:
            filepath = docs_path / cat / fname
            if not filepath.exists():
                self.warn(f"Source file missing: {cat}/{fname}")
                missing += 1
                continue
            
            actual_hash = compute_file_hash(filepath)
            if actual_hash != stored_hash:
                self.warn(f"Hash mismatch (file changed since index built): {cat}/{fname}")
                mismatches += 1
            checked += 1
        
        if mismatches == 0 and missing == 0:
            self.ok(f"All {checked} file hashes match")
        else:
            if mismatches > 0:
                self.warn(f"{mismatches} files changed since last index build — rebuild recommended")
            if missing > 0:
                self.warn(f"{missing} source files not found in {self.docs_dir}")
        
        conn.close()
    
    def check_build_info(self):
        print("\n[8] Build metadata check")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT key, value FROM build_info")
            info = dict(cur.fetchall())
            
            for key in ['build_date', 'article_count', 'section_count', 'index_entries']:
                if key in info:
                    self.ok(f"{key}: {info[key]}")
                else:
                    self.warn(f"Missing build info key: {key}")
            
            if info.get('error_count', '0') != '0':
                self.warn(f"Build had {info['error_count']} errors")
        except Exception as e:
            self.warn(f"Could not read build info: {e}")
        
        conn.close()
    
    def run_all(self):
        print(f"{'='*60}")
        print(f"SurvivalAI Index Verification")
        print(f"Database: {self.db_path}")
        if self.docs_dir:
            print(f"Docs dir: {self.docs_dir}")
        print(f"{'='*60}")
        
        if not self.check_db_exists():
            print(f"\n{'='*60}")
            print(f"ABORTED: Database not found. Run build_index.py first.")
            return False
        
        self.check_integrity()
        self.check_tables()
        self.check_article_counts()
        self.check_sections()
        self.check_fts_search()
        self.check_build_info()
        
        if self.docs_dir and os.path.isdir(self.docs_dir):
            self.check_file_hashes()
        
        # Summary
        print(f"\n{'='*60}")
        print(f"RESULTS")
        print(f"  Passed:   {self.passed}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Errors:   {len(self.errors)}")
        
        if self.errors:
            print(f"\n  VERDICT: FAIL — {len(self.errors)} error(s) must be fixed")
            return False
        elif self.warnings:
            print(f"\n  VERDICT: PASS with warnings — review items above")
            return True
        else:
            print(f"\n  VERDICT: PASS — all checks passed")
            return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Verify SurvivalAI FTS5 search index')
    parser.add_argument('--db', default='./search/knowledge.db', help='Path to database')
    parser.add_argument('--docs-dir', default=None, help='Path to docs directory (for hash verification)')
    args = parser.parse_args()
    
    verifier = Verifier(args.db, args.docs_dir)
    success = verifier.run_all()
    sys.exit(0 if success else 1)
