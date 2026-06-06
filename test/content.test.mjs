import test from "node:test";
import assert from "node:assert/strict";

import {
  mentors,
  noticeGroups,
  serviceCategories,
  siteMeta,
} from "../src/content.js";

test("site metadata matches the esports studio brief", () => {
  assert.equal(siteMeta.title, "混水电竞｜三角洲行动护航工作室");
  assert.match(siteMeta.description, /未成年人禁止下单/);
  assert.match(siteMeta.keywords, /混水电竞/);
  assert.match(siteMeta.keywords, /三角洲行动护航/);
});

test("all requested service categories are present without direct prices", () => {
  const names = serviceCategories.map((item) => item.name);

  assert.deepEqual(names, [
    "特惠单",
    "保底单",
    "清图单",
    "红单",
    "特色卡单",
    "单局带出单",
    "圆梦必出单",
    "连续撤离单",
    "特色趣味单",
  ]);

  for (const item of serviceCategories) {
    assert.equal("price" in item, false);
    assert.ok(item.description.length >= 18);
  }
});

test("notice copy keeps risks visible and avoids gambling-style wording", () => {
  const allNoticeText = noticeGroups
    .flatMap((group) => [group.title, ...group.items])
    .join("\n");

  assert.match(allNoticeText, /未成年人禁止下单/);
  assert.match(allNoticeText, /理性消费/);
  assert.match(allNoticeText, /官方渠道/);

  for (const banned of ["红包", "转盘", "包赢", "稳赚", "暴富", "无脑上车"]) {
    assert.doesNotMatch(allNoticeText, new RegExp(banned));
  }
});

test("mentor list contains every named mentor", () => {
  assert.deepEqual(
    mentors.map((mentor) => mentor.name),
    ["小穗", "十一", "小慧", "庸颜", "黑桃", "残念", "二代"],
  );
});
