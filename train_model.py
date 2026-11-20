"""One-variable ordinary least squares, using only Python's standard library."""
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import mean


def fit(rows):
    xs, ys = zip(*rows)
    if len(rows) < 2 or not all(math.isfinite(v) for row in rows for v in row):
        raise ValueError('Need at least two finite observations')
    mx, my = mean(xs), mean(ys)
    denominator = sum((x - mx) ** 2 for x in xs)
    if denominator == 0:
        raise ValueError('Experience must vary')
    slope = sum((x - mx) * (y - my) for x, y in rows) / denominator
    return slope, my - slope * mx


def main():
    source = Path(__file__).with_name('training_data.csv')
    with source.open(newline='', encoding='utf-8') as f:
        rows = [(float(r['YearsExperience']), float(r['Salary'])) for r in csv.DictReader(f)]
    # Every fifth row is held out; test rows never influence fitting.
    train = [row for i, row in enumerate(rows) if i % 5 != 0]
    test = [row for i, row in enumerate(rows) if i % 5 == 0]
    slope, intercept = fit(train)
    mse = mean((slope * x + intercept - y) ** 2 for x, y in test)
    baseline_mse = mean((mean([y for _, y in train]) - y) ** 2 for _, y in test)
    if mse >= baseline_mse:
        raise ValueError('Model does not beat the training-mean baseline on held-out rows')
    out = Path(__file__).with_name('dist')
    out.mkdir(exist_ok=True)
    model = {'algorithm': 'ordinary_least_squares', 'feature': 'YearsExperience',
             'target': 'Salary', 'coefficient': slope, 'intercept': intercept,
             'training_rows': len(train), 'data_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
    metrics = {'test_rows': len(test), 'test_mse': mse, 'test_rmse': math.sqrt(mse),
               'baseline_test_mse': baseline_mse, 'split': 'index modulo 5 == 0 is held out'}
    (out / 'linear_model.json').write_text(json.dumps(model, indent=2) + '\n', encoding='utf-8')
    (out / 'metrics.json').write_text(json.dumps(metrics, indent=2) + '\n', encoding='utf-8')
    (out / 'linear_model.txt').write_text(f'Coefficient: {slope}\nIntercept: {intercept}\n', encoding='utf-8')
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()
