#!/usr/bin/env python3
"""
Planning Validation Script
Cross-checks data between planning_by_group.md and planning_chronological.md
"""

import re
from pathlib import Path
from collections import defaultdict

def parse_planning_by_group(file_path):
    """Parse planning_by_group.md and extract all sessions"""
    sessions = []
    current_group = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        # Detect group header
        if line.startswith('## 📊 Groupe'):
            match = re.search(r'Groupe ([\w\s]+) \(', line)
            if match:
                current_group = match.group(1).strip()
        
        # Parse session row
        if current_group and line.startswith('|') and 'TD0' in line or 'TD1' in line or 'TD2' in line or 'TD3' in line or 'TD4' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 8 and parts[1] and not parts[1].startswith('Date'):
                sessions.append({
                    'group': current_group,
                    'date': parts[1],
                    'day': parts[2],
                    'time': parts[3],
                    'duration': parts[4],
                    'td': parts[5],
                    'content': parts[6],
                    'cumulative': parts[7]
                })
    
    return sessions

def parse_planning_chronological(file_path):
    """Parse planning_chronological.md and extract all sessions"""
    sessions = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_table = False
    for line in lines:
        if 'Toutes les séances TD' in line:
            in_table = True
            continue
        
        if in_table and line.startswith('|') and ('TD0' in line or 'TD1' in line or 'TD2' in line or 'TD3' in line or 'TD4' in line):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 9 and parts[1] and not parts[1].startswith('Date'):
                sessions.append({
                    'date': parts[1],
                    'group': parts[2],
                    'day': parts[3],
                    'time': parts[4],
                    'duration': parts[5],
                    'td': parts[6],
                    'content': parts[7],
                    'cumulative': parts[8]
                })
        
        if in_table and line.startswith('---'):
            break
    
    return sessions

def validate_plannings(by_group_sessions, chronological_sessions):
    """Cross-validate the two plannings"""
    errors = []
    warnings = []
    
    # Build lookup for chronological sessions
    chrono_lookup = {}
    for session in chronological_sessions:
        key = (session['group'], session['date'], session['time'])
        chrono_lookup[key] = session
    
    # Build lookup for by_group sessions
    group_lookup = {}
    for session in by_group_sessions:
        key = (session['group'], session['date'], session['time'])
        group_lookup[key] = session
    
    print(f"\n=== Validation des plannings ===")
    print(f"Sessions dans planning_by_group.md: {len(by_group_sessions)}")
    print(f"Sessions dans planning_chronological.md: {len(chronological_sessions)}")
    
    # Check 1: All sessions from by_group exist in chronological
    print("\n--- Vérification 1: Présence de toutes les séances ---")
    for session in by_group_sessions:
        key = (session['group'], session['date'], session['time'])
        if key not in chrono_lookup:
            errors.append(f"❌ Séance manquante dans chronologique: {session['group']} - {session['date']} {session['time']}")
    
    # Check 2: All sessions from chronological exist in by_group
    for session in chronological_sessions:
        key = (session['group'], session['date'], session['time'])
        if key not in group_lookup:
            errors.append(f"❌ Séance manquante dans par groupe: {session['group']} - {session['date']} {session['time']}")
    
    if not errors:
        print("✓ Toutes les séances sont présentes dans les deux fichiers")
    else:
        for error in errors:
            print(error)
    
    # Check 3: Data consistency for matching sessions
    print("\n--- Vérification 2: Cohérence des données ---")
    data_errors = []
    
    for session in by_group_sessions:
        key = (session['group'], session['date'], session['time'])
        if key in chrono_lookup:
            chrono = chrono_lookup[key]
            
            # Check day
            if session['day'] != chrono['day']:
                data_errors.append(f"❌ Jour différent: {session['group']} {session['date']} - "
                                 f"Par groupe: {session['day']}, Chronologique: {chrono['day']}")
            
            # Check duration
            if session['duration'] != chrono['duration']:
                data_errors.append(f"❌ Durée différente: {session['group']} {session['date']} - "
                                 f"Par groupe: {session['duration']}, Chronologique: {chrono['duration']}")
            
            # Check TD
            if session['td'] != chrono['td']:
                data_errors.append(f"❌ TD différent: {session['group']} {session['date']} - "
                                 f"Par groupe: {session['td']}, Chronologique: {chrono['td']}")
            
            # Check content
            if session['content'] != chrono['content']:
                data_errors.append(f"❌ Contenu différent: {session['group']} {session['date']} - "
                                 f"Par groupe: '{session['content']}', Chronologique: '{chrono['content']}'")
    
    if not data_errors:
        print("✓ Toutes les données sont cohérentes entre les deux fichiers")
    else:
        for error in data_errors:
            print(error)
    
    # Check 4: Group totals
    print("\n--- Vérification 3: Totaux par groupe ---")
    group_totals_by_group = defaultdict(int)
    group_totals_chrono = defaultdict(int)
    
    for session in by_group_sessions:
        group_totals_by_group[session['group']] += 1
    
    for session in chronological_sessions:
        group_totals_chrono[session['group']] += 1
    
    total_errors = []
    for group in sorted(set(list(group_totals_by_group.keys()) + list(group_totals_chrono.keys()))):
        count_by_group = group_totals_by_group.get(group, 0)
        count_chrono = group_totals_chrono.get(group, 0)
        
        if count_by_group == count_chrono:
            print(f"✓ {group}: {count_by_group} séances (cohérent)")
        else:
            total_errors.append(f"❌ {group}: Par groupe={count_by_group}, Chronologique={count_chrono}")
    
    for error in total_errors:
        print(error)
    
    # Check 5: Chronological order
    print("\n--- Vérification 4: Ordre chronologique ---")
    order_errors = []
    
    for i in range(1, len(chronological_sessions)):
        prev = chronological_sessions[i-1]
        curr = chronological_sessions[i]
        
        # Parse dates and times
        prev_datetime = f"{prev['date']} {prev['time'].split('-')[0]}"
        curr_datetime = f"{curr['date']} {curr['time'].split('-')[0]}"
        
        # Simple string comparison (works for DD/MM/YYYY HH:MM format if sorted)
        # For more robust check, parse to datetime objects
        from datetime import datetime
        try:
            prev_dt = datetime.strptime(prev_datetime, '%d/%m/%Y %H:%M')
            curr_dt = datetime.strptime(curr_datetime, '%d/%m/%Y %H:%M')
            
            if curr_dt < prev_dt:
                order_errors.append(f"❌ Ordre incorrect: {prev['date']} {prev['time']} ({prev['group']}) "
                                  f"après {curr['date']} {curr['time']} ({curr['group']})")
        except:
            warnings.append(f"⚠️  Impossible de vérifier l'ordre pour: {prev_datetime} vs {curr_datetime}")
    
    if not order_errors and not warnings:
        print("✓ Toutes les séances sont dans l'ordre chronologique")
    else:
        for error in order_errors:
            print(error)
        for warning in warnings:
            print(warning)
    
    # Summary
    print("\n=== Résumé ===")
    total_errors = len(errors) + len(data_errors) + len(total_errors) + len(order_errors)
    if total_errors == 0:
        print("✅ Les deux plannings sont parfaitement cohérents !")
    else:
        print(f"⚠️  {total_errors} erreur(s) détectée(s)")
    
    return total_errors == 0

def main():
    script_dir = Path(__file__).parent
    
    by_group_file = script_dir / 'planning_by_group.md'
    chronological_file = script_dir / 'planning_chronological.md'
    
    if not by_group_file.exists():
        print(f"Erreur: {by_group_file} introuvable")
        return
    
    if not chronological_file.exists():
        print(f"Erreur: {chronological_file} introuvable")
        return
    
    print("Lecture des fichiers de planning...")
    by_group_sessions = parse_planning_by_group(by_group_file)
    chronological_sessions = parse_planning_chronological(chronological_file)
    
    validate_plannings(by_group_sessions, chronological_sessions)

if __name__ == '__main__':
    main()
