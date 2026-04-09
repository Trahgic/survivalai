#!/usr/bin/env python3
"""
build_index.py — Build the FTS5 search index for SurvivalAI.

Scans all markdown files in docs/, parses frontmatter and content,
and builds a SQLite database with full-text search capabilities.

Usage:
    python3 build_index.py [--docs-dir ./docs] [--output ./search/knowledge.db] [--verbose]

This script is PRIVATE — not included in the public repo or shipped on the drive.
The resulting knowledge.db IS shipped.
"""

import sqlite3
import os
import re
import sys
import argparse
import hashlib
from pathlib import Path


def parse_frontmatter(text):
    """Extract YAML frontmatter from markdown content.
    
    Returns (metadata_dict, body_text).
    Handles the simple key: value format used in SurvivalAI articles.
    No external YAML dependency needed.
    """
    metadata = {}
    body = text
    
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            fm_block = parts[1].strip()
            body = parts[2].strip()
            
            for line in fm_block.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, _, value = line.partition(':')
                    key = key.strip().lower()
                    value = value.strip()
                    metadata[key] = value
    
    return metadata, body


def split_into_sections(body):
    """Split markdown body into sections based on ## headers.
    
    Returns list of (heading, content) tuples.
    The first section may have heading=None if content precedes the first header.
    """
    sections = []
    current_heading = None
    current_lines = []
    
    for line in body.split('\n'):
        if line.startswith('## '):
            # Save previous section
            if current_lines:
                content = '\n'.join(current_lines).strip()
                if content:
                    sections.append((current_heading, content))
            current_heading = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    
    # Save last section
    if current_lines:
        content = '\n'.join(current_lines).strip()
        if content:
            sections.append((current_heading, content))
    
    return sections


def clean_text(text):
    """Remove markdown formatting for plain-text indexing."""
    # Remove markdown links, keeping text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove bold/italic markers
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    # Remove inline code backticks
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove blockquote markers
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    # Remove heading markers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove horizontal rules
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
    # Remove table formatting pipes (but keep cell content)
    text = re.sub(r'\|', ' ', text)
    # Remove list markers
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    # Collapse whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()


def compute_file_hash(filepath):
    """SHA256 hash of file contents for change detection."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def build_database(docs_dir, output_path, verbose=False):
    """Build the FTS5 search database from markdown files."""
    
    docs_path = Path(docs_dir)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing database
    if output_file.exists():
        os.remove(output_file)
    
    conn = sqlite3.connect(str(output_file))
    cur = conn.cursor()
    
    # Create tables
    cur.executescript('''
        -- Article metadata
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            filename TEXT NOT NULL,
            title TEXT,
            source TEXT,
            tags TEXT,
            last_reviewed TEXT,
            file_hash TEXT,
            UNIQUE(category, filename)
        );
        
        -- FTS5 virtual table for full-text search with porter stemming
        CREATE VIRTUAL TABLE search_index USING fts5(
            article_id,
            category,
            title,
            section_heading,
            content,
            tags,
            tokenize='porter unicode61'
        );
        
        -- Section storage for retrieving specific passages
        CREATE TABLE sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            heading TEXT,
            content TEXT NOT NULL,
            position INTEGER NOT NULL,
            FOREIGN KEY (article_id) REFERENCES articles(id)
        );
        
        -- Build metadata
        CREATE TABLE build_info (
            key TEXT PRIMARY KEY,
            value TEXT
        );
    ''')
    
    # Scan for markdown files
    md_files = sorted(docs_path.rglob('*.md'))
    
    # Filter out INDEX.md and non-article files
    md_files = [f for f in md_files if f.name != 'INDEX.md' 
                and not f.name.startswith('.')
                and f.name != 'README.md']
    
    if verbose:
        print(f"Found {len(md_files)} markdown files in {docs_dir}")
    
    article_count = 0
    section_count = 0
    index_count = 0
    errors = []
    
    for md_file in md_files:
        try:
            rel_path = md_file.relative_to(docs_path)
            parts = rel_path.parts
            
            # Determine category from directory structure
            if len(parts) >= 2:
                category = parts[0]
            else:
                category = 'uncategorized'
            
            filename = md_file.name
            file_hash = compute_file_hash(md_file)
            
            # Read and parse
            with open(md_file, 'r', encoding='utf-8') as f:
                raw_text = f.read()
            
            metadata, body = parse_frontmatter(raw_text)
            title = metadata.get('title', filename.replace('.md', '').replace('-', ' ').title())
            source = metadata.get('source', '')
            tags = metadata.get('tags', '')
            last_reviewed = metadata.get('last_reviewed', '')
            
            # Insert article record
            cur.execute('''
                INSERT INTO articles (category, filename, title, source, tags, last_reviewed, file_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (category, filename, title, source, tags, last_reviewed, file_hash))
            article_id = cur.lastrowid
            article_count += 1
            
            # Split into sections and index each
            sections = split_into_sections(body)
            
            if not sections:
                # No sections — index the whole body as one chunk
                clean_body = clean_text(body)
                cur.execute('''
                    INSERT INTO sections (article_id, heading, content, position)
                    VALUES (?, ?, ?, ?)
                ''', (article_id, None, clean_body, 0))
                
                cur.execute('''
                    INSERT INTO search_index (article_id, category, title, section_heading, content, tags)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (str(article_id), category, title, '', clean_body, tags))
                section_count += 1
                index_count += 1
            else:
                for pos, (heading, content) in enumerate(sections):
                    clean_content = clean_text(content)
                    
                    # Store section
                    cur.execute('''
                        INSERT INTO sections (article_id, heading, content, position)
                        VALUES (?, ?, ?, ?)
                    ''', (article_id, heading, clean_content, pos))
                    section_count += 1
                    
                    # Index section
                    cur.execute('''
                        INSERT INTO search_index (article_id, category, title, section_heading, content, tags)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (str(article_id), category, title, heading or '', clean_content, tags))
                    index_count += 1
            
            if verbose:
                sec_count = len(sections) if sections else 1
                print(f"  [{category}] {filename} — {title} ({sec_count} sections)")
        
        except Exception as e:
            errors.append((str(md_file), str(e)))
            print(f"  ERROR: {md_file}: {e}", file=sys.stderr)
    
    # Store build metadata
    import datetime
    cur.execute("INSERT INTO build_info VALUES ('build_date', ?)", (datetime.datetime.now().isoformat(),))
    cur.execute("INSERT INTO build_info VALUES ('article_count', ?)", (str(article_count),))
    cur.execute("INSERT INTO build_info VALUES ('section_count', ?)", (str(section_count),))
    cur.execute("INSERT INTO build_info VALUES ('index_entries', ?)", (str(index_count),))
    cur.execute("INSERT INTO build_info VALUES ('docs_dir', ?)", (str(docs_dir),))
    cur.execute("INSERT INTO build_info VALUES ('error_count', ?)", (str(len(errors)),))
    
    # Optimize FTS index
    cur.execute("INSERT INTO search_index(search_index) VALUES('optimize')")
    
    conn.commit()
    
    # Print summary
    db_size = output_file.stat().st_size
    print(f"\n{'='*50}")
    print(f"Build complete: {output_path}")
    print(f"  Articles:     {article_count}")
    print(f"  Sections:     {section_count}")
    print(f"  Index entries: {index_count}")
    print(f"  Database size: {db_size / 1024:.1f} KB")
    print(f"  Errors:       {len(errors)}")
    
    if errors:
        print(f"\nErrors:")
        for path, err in errors:
            print(f"  {path}: {err}")
    
    # Quick sanity check
    cur.execute("SELECT count(*) FROM search_index WHERE search_index MATCH 'water'")
    water_hits = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM search_index WHERE search_index MATCH 'fire'")
    fire_hits = cur.fetchone()[0]
    print(f"\nSanity check:")
    print(f"  'water' matches: {water_hits} sections")
    print(f"  'fire' matches:  {fire_hits} sections")
    
    conn.close()
    return article_count, len(errors)


def example_queries(db_path):
    """Run a few example queries to demonstrate the search."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    print(f"\n{'='*50}")
    print("Example queries:\n")
    
    queries = [
        "wound infection antibiotic",
        "starting fire wet",
        "water purification bleach",
        "broken bone splint",
        "edible plants identification",
    ]
    
    for query in queries:
        cur.execute('''
            SELECT s.article_id, s.category, s.title, s.section_heading,
                   snippet(search_index, 4, '>>>', '<<<', '...', 30) as snippet,
                   rank
            FROM search_index s
            WHERE search_index MATCH ?
            ORDER BY rank
            LIMIT 3
        ''', (query,))
        
        results = cur.fetchall()
        print(f'  "{query}" → {len(results)} results')
        for r in results:
            print(f'    [{r[1]}] {r[2]} > {r[3] or "(intro)"}')
            print(f'    {r[4][:100]}...')
        print()
    
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build SurvivalAI FTS5 search index')
    parser.add_argument('--docs-dir', default='./docs', help='Path to docs directory')
    parser.add_argument('--output', default='./search/knowledge.db', help='Output database path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show per-file output')
    parser.add_argument('--examples', action='store_true', help='Run example queries after build')
    args = parser.parse_args()
    
    if not os.path.isdir(args.docs_dir):
        print(f"Error: docs directory not found: {args.docs_dir}", file=sys.stderr)
        sys.exit(1)
    
    count, errors = build_database(args.docs_dir, args.output, args.verbose)
    
    if args.examples:
        example_queries(args.output)
    
    sys.exit(1 if errors > 0 else 0)
