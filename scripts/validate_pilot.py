#!/usr/bin/env python3
"""Structural contract validation only; NEVER executes AI agents or app QA."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {'project_id','dna_version','task_id','agent','status','depends_on','artifact_links','assumptions','open_questions','risks','acceptance_criteria','evidence'}
STATUSES = {'PENDING','IN_PROGRESS','BLOCKED','READY_FOR_REVIEW','COMPLETED_VERIFIED','FAILED'}

def validate(root=ROOT, require_release=False):
    for f in ('README.md','CLAUDE.md','docs/project-dna.md','docs/project-dna.json','handoffs/state.json','release/README.md'):
        if not (root/f).is_file(): raise ValueError(f'Missing {f}')
    dna=json.loads((root/'docs/project-dna.json').read_text(encoding='utf-8'))
    state=json.loads((root/'handoffs/state.json').read_text(encoding='utf-8'))
    if dna.get('project_id') != state.get('project_id'): raise ValueError('Project IDs differ')
    if dna.get('version') != state.get('dna_version'): raise ValueError('DNA versions differ')
    if dna.get('approval_status') not in {'DRAFT','APPROVED'}: raise ValueError('Invalid approval status')
    approved=dna['approval_status']=='APPROVED' and bool(dna.get('approved_by')) and bool(dna.get('approved_at'))
    if dna['approval_status']=='APPROVED' and not approved: raise ValueError('Missing approval evidence')
    tasks=state.get('tasks')
    if not isinstance(tasks,list) or not tasks: raise ValueError('No tasks')
    ids=[x.get('task_id') for x in tasks]
    if len(ids)!=len(set(ids)): raise ValueError('Duplicate task IDs')
    for t in tasks:
        if not REQUIRED.issubset(t): raise ValueError('Invalid handoff schema')
        if t.get('project_id') != dna['project_id'] or t.get('dna_version') != dna['version']:
            raise ValueError('Stale handoff')
        if t['status'] not in STATUSES: raise ValueError('Invalid status')
        if any(d not in ids for d in t['depends_on']): raise ValueError('Unknown dependency')
        for key in ('artifact_links','assumptions','open_questions','risks','acceptance_criteria','evidence'):
            if not isinstance(t[key],list): raise ValueError('Expected handoff lists')
        if t['status']=='COMPLETED_VERIFIED' and not (t['evidence'] and t['artifact_links']):
            raise ValueError('Completion requires evidence and artifacts')
        if not approved and t['status'] not in ('PENDING','BLOCKED'):
            raise ValueError('DNA approval is required')
    by_id={t['task_id']:t for t in tasks}
    for t in tasks:
        if t['status'] in ('IN_PROGRESS','READY_FOR_REVIEW','COMPLETED_VERIFIED'):
            for dep in t['depends_on']:
                if by_id[dep]['status'] != 'COMPLETED_VERIFIED':
                    raise ValueError(f"Unverified prerequisite {dep} for {t['task_id']}")
    if require_release:
        if not approved: raise ValueError('Release blocked: DNA not approved')
        if not dna.get('live_deploy_authorized'): raise ValueError('Release blocked: no authorization')
        lookup={t['task_id']:t for t in tasks}
        for task_id in ('QA-001','QUAL-001','ORCH-RELEASE'):
            if lookup.get(task_id,{}).get('status')!='COMPLETED_VERIFIED':
                raise ValueError('Release blocked: missing independent gates')
    return {'project':dna['project_id'],'dna_approved':approved,'tasks':len(tasks),'release_authorized':bool(dna.get('live_deploy_authorized'))}

if __name__=='__main__':
    import sys
    try: print(json.dumps(validate(require_release='--release' in sys.argv), ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as e:
        print('EIXO PILOT BLOCKED:',e,file=sys.stderr);sys.exit(2)
