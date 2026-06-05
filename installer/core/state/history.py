"""History Engine"""



def save_history_snapshot(self, snapshot: Dict) -> None:
        import datetime

        ts = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        target = self.history_dir / f'{ts}.json'
        target.write_text(json.dumps(snapshot, indent=2), encoding='utf-8')

def latest_snapshot(self) -> Optional[Dict]:
        files = sorted(self.history_dir.glob('*.json'))
        if not files:
            return None

        return json.loads(files[-1].read_text(encoding='utf-8'))

def diff_against_previous(self, current: Dict) -> Dict:
        previous = self.latest_snapshot()

        if not previous:
            return {'available': False, 'changes': []}

        changes = []

        prev_score = previous.get('analysis', {}).get('score')
        curr_score = current.get('analysis', {}).get('score')

        if prev_score != curr_score:
            changes.append(
                f'health_score: {prev_score} -> {curr_score}'
            )

        return {
            'available': True,
            'changes': changes,
        }