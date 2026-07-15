<div align="center">

# kb-foundry · 知识铸造厂

> 把客户真实业务铸造成可运行、可验收、可回滚的知识库操作系统

**当前版本：v1.0-beta.3**

</div>

---

## 它不只是生成目录

普通知识库搭建往往停在“建了很多文件夹”。kb-foundry 负责的是完整交付链路：

```text
五维业务诊断
-> 选择 Lite / Standard / Full
-> 建立交付清单
-> 业务流与能力配置
-> 安全创建目录和规则
-> 机器校验
-> 首条真实业务流走查
-> 运行证据
-> 验收、回滚与升级
```

目录存在不代表系统能运行，模拟走查也不代表客户已经验收。

## v1.0-beta.3 新增

- `customer-kb-delivery/v1`：机器可读的客户交付清单。
- 六级运行阶段：`designed`、`scaffolded`、`walkthrough_ready`、`pilot_running`、`accepted`、`operational`。
- Lite / Standard / Full 的明确最低交付门槛。
- 安全搭建协议：先预览、再快照、再写入，禁止静默覆盖客户文件。
- 客户根目录校验器：检查路径、业务流、能力依赖、首跑证据、阶段、回滚和内部信息泄露。
- 修复本地搜索脚本，并增强中文短词检索。
- 律师事务所示例升级为可校验的 Standard、`walkthrough_ready` 交付包。

## 安装

```text
帮我安装这个 skill：https://github.com/ghostyee2023/kb-foundry
```

或：

```bash
npx skills add ghostyee2023/kb-foundry
```

## 怎么用

探索阶段：

```text
用 kb-foundry 帮我诊断一个企业培训客户，先不要写文件。
告诉我该用 Lite、Standard 还是 Full，并给出第一条业务流。
```

准备搭建：

```text
用 kb-foundry 在指定客户目录搭建 Standard 版。
先检查现有文件并输出 create / merge / keep / blocked 预览，我确认后再写。
```

审计已有知识库：

```text
用 kb-foundry 审计这个客户根目录，只诊断问题，不自动修复。
```

## 五维诊断

kb-foundry 先看五件事：

| 维度 | 要回答的问题 |
| --- | --- |
| 上下文 | 客户卖什么、服务谁、要什么结果、谁负责 |
| 资产 | 已有什么资料、在哪里、哪些敏感、哪些可复用 |
| 能力 | 每个业务节点需要什么动作、工具、权限和回退 |
| 业务流 | 输入怎样经过判断、处理、交付、复盘和回流 |
| 治理 | 什么不能自动化，怎样留证据、升级和回滚 |

## 三种交付规模

| 规模 | 适用情况 | 核心要求 |
| --- | --- | --- |
| Lite | 个人、小团队、试点 | 一条业务流、最小目录、能力开关、首跑记录 |
| Standard | 稳定业务、持续 AI 协作 | Lite + skill 层、权限边界、所有权、升级与快照 |
| Full | 组织级或付费转型交付 | Standard + 正式诊断、培训、交接、回滚和验收证据 |

规模不是越大越好。第一版只做能闭环的一条真实业务流。

## 运行阶段

```text
designed
-> scaffolded
-> walkthrough_ready
-> pilot_running
-> accepted
-> operational
```

每次只能升一级，并且先有证据、后改状态。

## 校验工具

验证客户根目录：

```bash
python scripts/validate_customer_kb.py --root <customer-root> --manifest <customer-root>/delivery-manifest.json
```

测试中文本地搜索：

```bash
python assets/scripts/hybrid_search.py --self-test
python assets/scripts/hybrid_search.py "客户交付" --root <customer-root>
```

两个脚本都是零依赖、本地运行。客户根目录校验器只读，不会修改文件。

## 律师事务所示例

`examples/lawyer-firm/` 展示了：

- 客户咨询到案件交付业务流。
- 律师人工确认与保密边界。
- 完整交付清单、能力依赖和回退。
- 首次走查记录。
- 可直接运行的客户根目录校验。

示例当前阶段是 `walkthrough_ready`，并未伪装成真实客户验收案例。

## 边界

- 不照抄 OPC 或其他客户的目录、路径和私人上下文。
- 不默认写文件，也不递归覆盖客户根目录。
- 搭建授权不等于允许安装 skill、同步平台、发送消息或对外交付。
- 不让 `blocked` 能力成为活动业务流的必需能力。
- 不用模拟数据声称客户已经接受或系统已经运营。
- 不确定的运行环境必须标记为 `manual` 或 `blocked`，并给人工回退。

## 验证状态

已验证：方法与模板结构、交付清单、规模/阶段门槛、校验器回归、中文搜索、律师示例机器校验和模拟前向测试。

待验证：多个行业的真实客户长期运行证据，以及从 `pilot_running` 到 `operational` 的重复交付数据。

## License

MIT，详见 `LICENSE`。
