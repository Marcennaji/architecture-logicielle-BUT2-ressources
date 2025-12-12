#!/usr/bin/env python3
"""
ICS Calendar Parser - Generate Teaching Schedule from ICS file

This script parses an ICS calendar file and generates two Markdown files:
1. Planning by group (separate tables per group)
2. Chronological planning (single merged table sorted by date/time)

The script:
- Handles timezone conversion (UTC to local time)
- Verifies weekday consistency
- Leaves "Suggested content" column empty for manual filling
- Is reusable for any ICS calendar format

Usage:
    python parse_ics_planning.py <input.ics> [--output-dir OUTPUT_DIR]

Requirements:
    pip install icalendar python-dateutil pytz
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

try:
    from icalendar import Calendar
    from dateutil import tz
    import pytz
except ImportError:
    print("Error: Required libraries not installed.")
    print("Please run: pip install icalendar python-dateutil pytz")
    sys.exit(1)


class ICSEvent:
    """Represents a calendar event with all necessary information"""
    
    def __init__(self, summary: str, start: datetime, end: datetime, location: str = ""):
        self.summary = summary
        self.start = start
        self.end = end
        self.location = location
        self.group = self._extract_group()
        self.event_type = self._extract_event_type()
        self.duration_hours = (end - start).total_seconds() / 3600
        
    def _extract_group(self) -> str:
        """Extract group identifier from summary (e.g., '2A I', '2B I')"""
        summary_upper = self.summary.upper()
        
        # Pattern: "2X I" where X is A, B, C, D, etc.
        for char in ['A', 'B', 'C', 'D', 'E', 'F']:
            pattern = f"2{char} I"
            if pattern in summary_upper:
                return pattern.replace(' ', ' ')  # Normalize spacing
        
        # Check for CM (Cours Magistral)
        if 'CM' in summary_upper or 'AMPHI' in summary_upper or 'COURS MAGISTRAL' in summary_upper:
            return 'CM'
        
        return 'UNKNOWN'
    
    def _extract_event_type(self) -> str:
        """Determine if event is CM (lecture) or TD (tutorial)"""
        if self.group == 'CM':
            return 'CM'
        return 'TD'
    
    def get_weekday(self) -> str:
        """Get weekday name in French (abbreviated)"""
        days = {
            'Monday': 'Lun',
            'Tuesday': 'Mar', 
            'Wednesday': 'Mer',
            'Thursday': 'Jeu',
            'Friday': 'Ven',
            'Saturday': 'Sam',
            'Sunday': 'Dim'
        }
        return days[self.start.strftime('%A')]
    
    def get_date_str(self) -> str:
        """Get formatted date string (DD/MM/YYYY)"""
        return self.start.strftime('%d/%m/%Y')
    
    def get_time_range(self) -> str:
        """Get formatted time range (HH:MM-HH:MM)"""
        return f"{self.start.strftime('%H:%M')}-{self.end.strftime('%H:%M')}"
    
    def verify_weekday(self) -> Tuple[bool, str]:
        """
        Verify that the date matches expected weekday
        Returns: (is_valid, expected_weekday)
        """
        actual_weekday = self.start.strftime('%A')
        expected_weekday = self.get_weekday()
        
        days_map = {
            'Lun': 'Monday', 'Mar': 'Tuesday', 'Mer': 'Wednesday',
            'Jeu': 'Thursday', 'Ven': 'Friday', 'Sam': 'Saturday', 'Dim': 'Sunday'
        }
        
        is_valid = days_map.get(expected_weekday) == actual_weekday
        return is_valid, expected_weekday


class ICSParser:
    """Parse ICS calendar file and extract teaching events"""
    
    def __init__(self, ics_path: Path, target_timezone: str = 'Europe/Paris'):
        self.ics_path = ics_path
        self.target_tz = pytz.timezone(target_timezone)
        self.events: List[ICSEvent] = []
        
    def parse(self) -> List[ICSEvent]:
        """Parse ICS file and return list of events"""
        with open(self.ics_path, 'rb') as f:
            cal = Calendar.from_ical(f.read())
        
        for component in cal.walk():
            if component.name == "VEVENT":
                event = self._parse_event(component)
                if event:
                    self.events.append(event)
        
        # Sort events by start time
        self.events.sort(key=lambda e: e.start)
        
        # Verify weekdays
        self._verify_all_weekdays()
        
        return self.events
    
    def _parse_event(self, component) -> ICSEvent:
        """Parse single VEVENT component"""
        try:
            summary = str(component.get('SUMMARY', ''))
            location = str(component.get('LOCATION', ''))
            
            # Get start and end times
            dtstart = component.get('DTSTART').dt
            dtend = component.get('DTEND').dt
            
            # Convert to datetime if date only
            if not isinstance(dtstart, datetime):
                dtstart = datetime.combine(dtstart, datetime.min.time())
            if not isinstance(dtend, datetime):
                dtend = datetime.combine(dtend, datetime.min.time())
            
            # Convert to target timezone
            if dtstart.tzinfo is None:
                dtstart = pytz.UTC.localize(dtstart)
            if dtend.tzinfo is None:
                dtend = pytz.UTC.localize(dtend)
                
            dtstart = dtstart.astimezone(self.target_tz)
            dtend = dtend.astimezone(self.target_tz)
            
            return ICSEvent(summary, dtstart, dtend, location)
            
        except Exception as e:
            print(f"Warning: Failed to parse event: {e}")
            return None
    
    def _verify_all_weekdays(self):
        """Verify weekdays for all events and print warnings"""
        print("\n=== Weekday Verification ===")
        errors_found = False
        
        for event in self.events:
            is_valid, expected = event.verify_weekday()
            if not is_valid:
                actual = event.start.strftime('%A')
                print(f"⚠️  ERROR: {event.get_date_str()} - Expected {expected} but is {actual}")
                print(f"    Event: {event.summary}")
                errors_found = True
        
        if not errors_found:
            print("✓ All weekdays verified successfully")
        print()
    
    def get_events_by_group(self) -> Dict[str, List[ICSEvent]]:
        """Group events by group identifier"""
        grouped = defaultdict(list)
        for event in self.events:
            grouped[event.group].append(event)
        return dict(grouped)


class MarkdownGenerator:
    """Generate Markdown planning files from parsed events"""
    
    def __init__(self, events: List[ICSEvent], teacher_name: str = ""):
        self.events = events
        self.teacher_name = teacher_name
        
    def generate_by_group(self, output_path: Path):
        """Generate planning file organized by group"""
        parser = ICSParser(Path())  # Dummy for grouping
        parser.events = self.events
        grouped = parser.get_events_by_group()
        
        # Separate CM from TD groups
        cm_events = grouped.pop('CM', [])
        td_groups = {k: v for k, v in grouped.items() if k != 'UNKNOWN'}
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Planning TD - Par groupe\n\n")
            
            if self.teacher_name:
                f.write(f"> Enseignant : {self.teacher_name}\n\n")
            
            # CM section
            if cm_events:
                f.write("## 📅 Cours magistraux (CM - Commun à tous les groupes)\n\n")
                f.write("| Date | Jour | Heure | Durée | Salle | Contenu |\n")
                f.write("|------|------|-------|--------|-------|---------|\n")
                
                for event in cm_events:
                    f.write(f"| {event.get_date_str()} | {event.get_weekday()} | "
                           f"{event.get_time_range()} | {event.duration_hours:.0f}h | "
                           f"{event.location} | {event.summary} |\n")
                f.write("\n---\n\n")
            
            # TD groups
            for group_name in sorted(td_groups.keys()):
                events = td_groups[group_name]
                total_hours = sum(e.duration_hours for e in events)
                
                f.write(f"## 📊 Groupe {group_name} ({len(events)} séances × 2h = {total_hours:.0f}h)\n\n")
                f.write("| Date | Jour | Heure | Durée | TD | Contenu suggéré | Heures cumulées |\n")
                f.write("|------|------|-------|--------|----|--------------------|-------------------|\n")
                
                cumulative = 0
                for event in events:
                    cumulative += event.duration_hours
                    f.write(f"| {event.get_date_str()} | {event.get_weekday()} | "
                           f"{event.get_time_range()} | {event.duration_hours:.0f}h | "
                           f" | | {cumulative:.0f}h |\n")
                
                f.write(f"\n**Total présentiel : {total_hours:.0f}h** ({len(events)} séances)\n\n")
                f.write("---\n\n")
        
        print(f"✓ Generated: {output_path}")
    
    def generate_chronological(self, output_path: Path):
        """Generate chronological planning file (single merged table)"""
        parser = ICSParser(Path())
        parser.events = self.events
        grouped = parser.get_events_by_group()
        
        # Separate CM from TDs
        cm_events = grouped.pop('CM', [])
        td_events = [e for events in grouped.values() for e in events if e.group != 'UNKNOWN']
        td_events.sort(key=lambda e: (e.start, e.group))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Planning TD - Vue chronologique\n\n")
            
            if self.teacher_name:
                f.write(f"> Enseignant : {self.teacher_name}\n\n")
            
            # CM section
            if cm_events:
                f.write("## 📅 Cours magistraux (CM)\n\n")
                f.write("| Date | Jour | Heure | Durée | Salle | Contenu |\n")
                f.write("|------|------|-------|--------|-------|---------|\n")
                
                for event in cm_events:
                    f.write(f"| {event.get_date_str()} | {event.get_weekday()} | "
                           f"{event.get_time_range()} | {event.duration_hours:.0f}h | "
                           f"{event.location} | {event.summary} |\n")
                f.write("\n---\n\n")
            
            # Chronological TD table
            f.write("## 📊 Toutes les séances TD (par ordre chronologique)\n\n")
            f.write("| Date | Groupe | Jour | Heure | Durée | TD | Contenu suggéré | Heures cumulées |\n")
            f.write("|------|--------|------|-------|--------|----|--------------------|-------------------|\n")
            
            # Track cumulative hours globally (chronological total)
            cumulative_total = 0
            group_hours = defaultdict(float)
            
            for event in td_events:
                cumulative_total += event.duration_hours
                group_hours[event.group] += event.duration_hours
                f.write(f"| {event.get_date_str()} | {event.group} | {event.get_weekday()} | "
                       f"{event.get_time_range()} | {event.duration_hours:.0f}h | "
                       f" | | {cumulative_total:.0f}h |\n")
            
            # Statistics
            f.write("\n---\n\n")
            f.write("## 📊 Statistiques\n\n")
            f.write(f"- **Total séances** : {len(cm_events) + len(td_events)} ")
            f.write(f"({len(cm_events)} CM + {len(td_events)} TD)\n")
            
            for group in sorted(group_hours.keys()):
                f.write(f"- **Groupe {group}** : {group_hours[group]:.0f}h\n")
        
        print(f"✓ Generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Parse ICS calendar and generate teaching schedule files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python parse_ics_planning.py calendar.ics
  python parse_ics_planning.py calendar.ics --output-dir ./output
  python parse_ics_planning.py calendar.ics --teacher "John Doe"
        """
    )
    
    parser.add_argument('ics_file', type=Path, help='Input ICS calendar file')
    parser.add_argument('--output-dir', type=Path, default=Path('.'),
                       help='Output directory for generated files (default: current directory)')
    parser.add_argument('--teacher', type=str, default='',
                       help='Teacher name to include in header')
    parser.add_argument('--timezone', type=str, default='Europe/Paris',
                       help='Target timezone (default: Europe/Paris)')
    
    args = parser.parse_args()
    
    # Validate input
    if not args.ics_file.exists():
        print(f"Error: File not found: {args.ics_file}")
        sys.exit(1)
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n=== ICS Calendar Parser ===")
    print(f"Input file: {args.ics_file}")
    print(f"Target timezone: {args.timezone}")
    print(f"Output directory: {args.output_dir}\n")
    
    # Parse ICS file
    print("Parsing ICS file...")
    ics_parser = ICSParser(args.ics_file, args.timezone)
    events = ics_parser.parse()
    print(f"✓ Found {len(events)} events\n")
    
    # Generate output files
    generator = MarkdownGenerator(events, args.teacher)
    
    output_by_group = args.output_dir / 'planning_by_group.md'
    output_chrono = args.output_dir / 'planning_chronological.md'
    
    print("Generating output files...")
    generator.generate_by_group(output_by_group)
    generator.generate_chronological(output_chrono)
    
    print("\n✓ Done! Files generated successfully.")
    print(f"\nNext steps:")
    print(f"1. Review the generated files")
    print(f"2. Fill in the 'Contenu suggéré' and 'TD' columns manually")
    print(f"3. Adjust formatting as needed\n")


if __name__ == '__main__':
    main()
