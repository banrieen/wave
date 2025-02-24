# 智能数据加载模块

在时空中探索和发现！

时间：更早的预知，筹划
空间：更广的探索，回溯

spray（浪花）-》 wave (波动)

## 业务故事线

1. 连接数据源
2. 构造数据
3. 在线图表
4. 导出数据

## 系统结构

提供 SaaS restful API，管道数据流。开放组件支持多样化的数据处理需求。

### Support CLI and restful api

![架构图](doc/waveFlow框架.dio)

* 基础业务数据默认选择 Mariadb(Mysql)
* 需要用到键值数据，默认 SQLite
* 缓存数据默认： Memcached
* 绘图组件：plotly, trednlines: statsmodels
* 导出为图像或html: kaleido

* 基于 sanic 支持 https 服务给到前端
* 基于 gRPC 支持其他语言调用
* 使用 uv 管理依赖和项目
* 教学动画：manim 
* 3D 模型：guesses