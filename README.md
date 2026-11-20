# Linear Model CI/CD

Repository: https://github.com/yei-241/linear-model-cicd

Practice 2: train a linear regression model from working-experience and salary data, then publish the model files with GitHub Actions.

## Files

- `training_data.csv`: 31 observations, with `YearsExperience,Salary` as the header.
- `train_model.py`: the original scikit-learn training script.
- `requirements.txt`: Python dependencies.
- `.github/workflows/ci-cd.yml`: automatic training and release workflow.

## Run locally

Install the requirements in your Python environment, then run the training script:

```bash
python -m pip install -r requirements.txt
python train_model.py
```

The script produces `linear_model.txt` (readable coefficients) and `linear_model.pkl` (the saved model). The data is a teaching example and does not establish the model's reliability for real salary prediction.

## Run on GitHub

1. Commit the files to the `main` branch. A push starts the workflow automatically.
2. Alternatively, open **Actions → CI/CD Pipeline → Run workflow**, select **main**, and confirm **Run workflow**.
3. Wait until the `train` and `publish` jobs both succeed.
4. Open **Releases** and download `linear_model.txt` and `linear_model.pkl` from the generated version.

This workflow uses the repository's automatically provided `GITHUB_TOKEN`. No personal access token is needed. Only the publication job has `contents: write`. Pull requests train and save an artifact but do not publish a release. Releases point to the source commit used for training; a separate `release` branch is not required.

## What was repaired

- Added the missing CSV header so pandas keeps the first observation as training data. Preserved the added 11.0-year / 126000 salary observation, for 31 observations in total.
- Added a manual-run entry and removed the data-change gate. Editing only the workflow or rerunning it can now produce a model as well.
- Publish both the text coefficients and the serialized model after training succeeds.
- Include the run attempt in the version tag so a rerun does not collide with the previous attempt's tag.

## Submission

After checking a successful Actions run and its Release attachments, submit:

https://github.com/yei-241/linear-model-cicd

## Useful explanations

- **CI** runs the training process automatically after changes and checks whether it succeeds.
- **CD** delivers the resulting model files through a GitHub Release.
- A workflow **artifact** belongs to a workflow run; a **Release** provides the versioned delivery page required for this exercise.
- The CSV header describes the columns. Without it, default `pandas.read_csv` treats the first observation as the header and drops it from the data.
- Job permissions and trigger conditions prevent pull requests from publishing releases.
