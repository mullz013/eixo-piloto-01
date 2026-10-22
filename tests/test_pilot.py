import json
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.validate_pilot import ROOT, validate

REQUIRED=['README.md','CLAUDE.md','docs/project-dna.md','docs/project-dna.json','handoffs/state.json','release/README.md']

class HandoffContracts(unittest.TestCase):
    def test_approved_briefing_contract(self):
        outcome=validate()
        self.assertTrue(outcome['dna_approved'])
        self.assertEqual(outcome['tasks'],8)
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
            p=root/'handoffs/state.json';state=json.loads(p.read_text())
            state['tasks'][0].update(status='COMPLETED_VERIFIED',evidence=[],artifact_links=[]);p.write_text(json.dumps(state))
            with self.assertRaises(ValueError):validate(root)
    def test_unapproved_in_progress(self):
        td,root=self.make_copy()
        with td:
            p=root/'docs/project-dna.json';dna=json.loads(p.read_text());dna['approval_status']='DRAFT';dna['approved_by']=None;dna['approved_at']=None;p.write_text(json.dumps(dna))
            p=root/'handoffs/state.json';state=json.loads(p.read_text());state['tasks'][1]['status']='IN_PROGRESS';p.write_text(json.dumps(state))
            with self.assertRaisesRegex(ValueError,'DNA approval'): validate(root)
    def test_missing_approval_record(self):
        td,root=self.make_copy()
        with td:
            p=root/'docs/project-dna.json';dna=json.loads(p.read_text());dna['approved_by']=None;p.write_text(json.dumps(dna))
            with self.assertRaisesRegex(ValueError,'approval evidence'):validate(root)

    def test_block_task_before_verified_dependencies(self):
        td,root=self.make_copy()
        with td:
            p=root/'handoffs/state.json';state=json.loads(p.read_text())
            state['tasks'][0]['status']='BLOCKED';state['tasks'][1]['status']='IN_PROGRESS';p.write_text(json.dumps(state))
            with self.assertRaisesRegex(ValueError,'prerequisite'): validate(root)

    def test_orchestrator_runtime_verified_with_evidence(self):
        state=json.loads((ROOT/'handoffs/state.json').read_text())
        orch=state['tasks'][0]
        self.assertEqual(orch['status'],'COMPLETED_VERIFIED')
        self.assertEqual(state['status'],'DNA_APPROVED_RUNTIME_VERIFIED')
        for rel in orch['artifact_links']:
            self.assertTrue((ROOT/rel).is_file(),rel)
        transcript=json.loads((ROOT/'evidence/ORCH-001/delegation-transcript.json').read_text())
        calls=[e for e in transcript if e['event']=='tool_use' and e['tool']=='Agent']
        self.assertEqual(calls[0]['input']['subagent_type'],'eixo-ux-architect')
        self.assertTrue(any(e.get('parent_tool_use_id')==calls[0]['id'] for e in transcript))

if __name__=='__main__':unittest.main()

