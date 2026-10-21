import json
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.validate_pilot import ROOT, validate

REQUIRED=['README.md','CLAUDE.md','docs/project-dna.md','docs/project-dna.json','handoffs/state.json','release/README.md']

class HandoffContracts(unittest.TestCase):
    def test_initial_draft_contract(self):
        outcome=validate()
        self.assertFalse(outcome['dna_approved'])
        self.assertEqual(outcome['tasks'],7)
    def test_release_blocked(self):
        with self.assertRaisesRegex(ValueError,'Release blocked'):
            validate(require_release=True)
    def make_copy(self):
        td=tempfile.TemporaryDirectory()
        root=Path(td.name)
        for f in REQUIRED:
            target=root/f;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/f,target)
        return td,root
    def test_duplicate_task(self):
        td,root=self.make_copy()
        with td:
            p=root/'handoffs/state.json';state=json.loads(p.read_text());state['tasks'].append(state['tasks'][0]);p.write_text(json.dumps(state))
            with self.assertRaisesRegex(ValueError,'Duplicate'): validate(root)
    def test_unverified_completion(self):
        td,root=self.make_copy()
        with td:
            p=root/'handoffs/state.json';state=json.loads(p.read_text());state['tasks'][0]['status']='COMPLETED_VERIFIED';p.write_text(json.dumps(state))
            with self.assertRaises(ValueError):validate(root)
    def test_unapproved_in_progress(self):
        td,root=self.make_copy()
        with td:
            p=root/'handoffs/state.json';state=json.loads(p.read_text());state['tasks'][1]['status']='IN_PROGRESS';p.write_text(json.dumps(state))
            with self.assertRaisesRegex(ValueError,'DNA approval'): validate(root)
    def test_missing_approval_record(self):
        td,root=self.make_copy()
        with td:
            p=root/'docs/project-dna.json';dna=json.loads(p.read_text());dna['approval_status']='APPROVED';p.write_text(json.dumps(dna))
            with self.assertRaisesRegex(ValueError,'approval evidence'):validate(root)

if __name__=='__main__':unittest.main()
