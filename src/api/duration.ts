import parse from "parse-duration";

export class Duration {
  minutes: number;

  constructor(minutes: number) {
    if (minutes < 0 || !Number.isInteger(minutes)) {
      throw new Error(`Invalid duration: ${minutes}`);
    }

    this.minutes = minutes;
  }

  public static parse(input: string): Duration | undefined {
    const parsedDuration = parse(input, "m");
    if (parsedDuration === undefined) {
      return undefined;
    }
    return new Duration(Math.floor(parsedDuration));
  }

  public humanized(
    cfg: {
      hours?: string;
      minutes?: string;
      space?: string;
      separator?: string;
    } = {}
  ): string {
    const space = cfg.space ?? "";
    const hoursSym = cfg.hours ?? "h";
    const minutesSym = cfg.minutes ?? "m";
    const separator = cfg.separator ?? " ";

    if (this.minutes < 60) {
      return `${this.minutes}${space}${minutesSym}`;
    }
    const hoursPart = Math.floor(this.minutes / 60);
    const minutesPart = this.minutes % 60;
    if (minutesPart === 0) {
      return `${hoursPart}${space}${hoursSym}`;
    }
    return `${hoursPart}${space}${hoursSym}${separator}${minutesPart}${space}${minutesSym}`;
  }
}
