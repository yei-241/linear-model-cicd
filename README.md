# Practice 2 机器学习模型自动训练与发布

作者：姚其其 / Seven17777

本项目使用课程提供的工作年限与薪资样例数据，训练一元线性回归模型。使用 Python 标准库实现普通最小二乘，无须安装第三方依赖。仅用于课程演示。

本地运行：`python train_model.py`。结果写入 `dist/`：`linear_model.json`、`linear_model.txt` 和 `metrics.json`。

## 验收

1. 打开 Actions，检查 Train and release linear model 的绿色运行记录。
2. 打开 Releases，下载三个资产文件。只有 Actions artifact 并不等于完成 Release 交付。
3. 修改训练数据并推送到 main，会再次训练并生成新版本。也可在 Actions 中手动运行。

## 原理与答辩

- CI：每次 push/PR 自动训练和验证。CD：验证成功后，在 main 的 push 或手动运行中发布 Release。
- 斜率等于协方差分子除以自变量离差平方和，截距为目标均值减去斜率乘自变量均值。
- 每第 5 行作为测试数据，不参与拟合；评价要求优于始终预测训练集薪资均值的基线。测试 RMSE 反映误差量纲，不能当作真实业务泛化保证。
- 发布文件记录数据 SHA256，Release tag 指向源代码提交，可以追溯训练数据和代码版本。
- PR 只构建验证，不发布；只有 release job 有 contents: write 权限。
- Artifact 是一次工作流的构建产物，Release 是带版本标签的交付入口；release 分支本身不等于 GitHub Release。
- 与课程示例的差异：无需强制覆盖 release 分支，直接将验证后的模型作为 Release 附件发布；符合老师按最终产物验收的要求。

数据来源：https://gitee.com/lundechen/data_engineering_master_2026_fall/blob/master/session-2/practice-2-ci-cd-github-actions-release.md


参考来源：[Seven17777/session2-practice-ci-cd](https://github.com/Seven17777/session2-practice-ci-cd)。
