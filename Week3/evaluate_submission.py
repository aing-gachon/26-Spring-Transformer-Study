"""운영자 전용: 신뢰할 수 있는 공통 노트북으로 제출 폴더를 평가합니다.

Colab T4에 노트북과 이 파일을 함께 두고 실행:
python evaluate_submission.py submission_folder --expected-package 공지한_DATA_PACKAGE
압축은 별도로 확인해서 해제합니다. 노트북 STEP7에 출력된 test 결과를 제출 파일로 재검증할 때 사용할 수 있습니다.
"""
import argparse
import hashlib
import json
from pathlib import Path


def load_runtime():
    notebook = next(Path(__file__).parent.glob('*.ipynb'))
    env = {}
    for cell in json.loads(notebook.read_text())['cells']:
        if 'league-definition' in cell.get('metadata', {}).get('tags', []):
            exec(''.join(cell['source']), env)
    return env


def evaluate_submission(folder, expected_package, env):
    folder = Path(folder)
    env['require_t4']()
    hashes = json.loads((folder / 'checksums.json').read_text())
    required = {'best.pt', 'summary.json', 'tokenizer.json', 'data_manifest.json'}
    if set(hashes) != required:
        raise ValueError('제출 파일 목록 불일치')
    for name in required:
        if hashlib.sha256((folder / name).read_bytes()).hexdigest() != hashes[name]:
            raise ValueError(f'파일 해시 불일치: {name}')
    summary = json.loads((folder / 'summary.json').read_text())
    manifest = json.loads((folder / 'data_manifest.json').read_text())
    protocol = env['PROTOCOL']
    if summary['protocol'] != protocol or manifest['protocol'] != protocol:
        raise ValueError('공통 프로토콜 불일치')
    if env['digest'](manifest) != expected_package or summary['package_id'] != expected_package:
        raise ValueError('공통 데이터 패키지 불일치')
    if not env['training_completed'](summary) or not summary['official_environment']:
        raise ValueError('T4 full 정상 종료(최대 updates 또는 early stopping) 기록이 필요합니다.')
    tok = env['Tokenizer'].from_file(str(folder / 'tokenizer.json'))
    if hashlib.sha256(tok.to_str().encode()).hexdigest() != manifest['tokenizer_hash']:
        raise ValueError('토크나이저 불일치')
    state = env['torch'].load(folder / 'best.pt', map_location='cpu', weights_only=True)
    identity = {k: summary[k] for k in ('architecture', 'training_hp', 'seed', 'package_id', 'protocol')}
    if state['identity'] != identity or env['digest'](identity)[:16] != summary['run_id']:
        raise ValueError('모델·실험 식별자 불일치')
    selected = [m for m in summary['history'] if m['step'] == state['step']]
    if len(selected) != 1 or selected[0]['bleu'] != state['metrics']['bleu']:
        raise ValueError('체크포인트 선택 이력 불일치')
    if state['metrics']['bleu'] != max(m['bleu'] for m in summary['history']):
        raise ValueError('최고 validation 체크포인트가 아닙니다.')
    model = env['LeagueTransformer'](summary['architecture'], tok.get_vocab_size(), summary['training_hp']).to(env['DEVICE'])
    model.load_state_dict(state['model'], strict=True)
    if sum(p.numel() for p in model.parameters()) != summary['parameters']:
        raise ValueError('파라미터 수 불일치')
    url = f"https://huggingface.co/datasets/bentrevett/multi30k/resolve/{protocol['dataset_revision']}/test.jsonl"
    with env['urlopen'](url, timeout=90) as response:
        payload = response.read()
    raw = [json.loads(line) for line in payload.decode().splitlines() if line.strip()]
    rows = [dict(src=[env['BOS']] + tok.encode(r['de']).ids[:protocol['max_length']-2] + [env['EOS']],
                 tgt=[env['BOS'], env['EOS']], reference=r['en']) for r in raw]
    metrics = env['evaluate_model'](model, rows, tok)
    result = dict(run_id=summary['run_id'], seed=summary['seed'], architecture=summary['architecture'],
                  package_id=expected_package, training_hp=summary['training_hp'], selected_step=state['step'],
                  test_sha256=hashlib.sha256(payload).hexdigest(), environment=env['environment'](), **metrics)
    (folder / 'operator_test_result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder')
    parser.add_argument('--expected-package', required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate_submission(args.folder, args.expected_package, load_runtime()), ensure_ascii=False, indent=2))
