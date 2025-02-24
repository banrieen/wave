-- Install lua and redis lib
-- sudo apt update -y 
-- sudo apt install -y luarocks lua5.1 liblua5.1-dev libssl-dev
-- sudo ln -s /usr/bin/lua5.1 /usr/local/bin/lua
-- sudo luarocks install redis-lua

-- 主脚本 main.lua

local redis = require("redis")
local client = redis.connect("10.0.56.113", 6379)
-- client:set("test_key", "hello_debian12")
-- print("Value:", client:get("test_key"))
-- client:quit()

-- 导入测试仪流程脚本tester_8200.lua, tester_V50.lua, tester_3360.lua, tester_3380D.lua,tester_3380P.lua
-- 实际先读取流程画布 json 配置，或系统配置 toml 导入，下面是示例内容。
local tester_8200 = require("tester_8200")
local tester_V50 = require("tester_V50")
local tester_3360 = require("tester_3360")
local tester_3380D = require("tester_3380D")
local tester_3380P = require("tester_3380P")


local flow_alarm = require("flow_alarm")
local datalog = require("datalog")

-- mian flow
function main()
    local raw_data = excel.load("data.xlsx")
    local cached_data = redis.get("latest_data")
    local merged = analyzer.merge(raw_data, cached_data)
    
    redis.set("latest_data", merged)
    local sorted = analyzer.sort(merged, "sales")
    
    excel.save(sorted, "analysis.xlsx")
    chart.create(sorted, "Sales Ranking")
end