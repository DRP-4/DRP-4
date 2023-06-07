import { describe, it, expect } from "vitest";
import { Duration } from "../duration";

describe("Duration", () => {
  it("parses", () => {
    expect(Duration.parse("10 minutes")).toMatchObject(new Duration(10));
    expect(Duration.parse("30 mins")).toMatchObject(new Duration(30));
    expect(Duration.parse("20 m")).toMatchObject(new Duration(20));
    expect(Duration.parse("1 h 30 mins")).toMatchObject(new Duration(90));
    expect(Duration.parse("1 h 30 mins something")).toMatchObject(
      new Duration(90)
    );
  });

  it("humanizes", () => {
    expect(new Duration(0).humanized()).toStrictEqual("0m");
    expect(new Duration(30).humanized()).toStrictEqual("30m");
    expect(new Duration(90).humanized()).toStrictEqual("1h 30m");
    expect(new Duration(60).humanized()).toStrictEqual("1h");
  });

  it("ignores seconds", () => {
    expect(Duration.parse("1s")).toMatchObject(new Duration(0));
  });
});
