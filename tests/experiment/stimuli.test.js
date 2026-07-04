import { describe, it, expect } from "vitest";
import { IMAGE_PATHS, VALIDATION_TRIALS } from "../../experiment/js/stimuli.js";
import { CONFIG } from "../../experiment/js/config.js";

describe("IMAGE_PATHS", () => {
  it("contains at least 3 images", () => {
    expect(IMAGE_PATHS.length).toBeGreaterThanOrEqual(3);
  });

  it("all paths start with assets/stimuli/", () => {
    for (const path of IMAGE_PATHS) {
      expect(path).toMatch(/^assets\/stimuli\//);
    }
  });

  it("all paths end with .png", () => {
    for (const path of IMAGE_PATHS) {
      expect(path).toMatch(/\.png$/);
    }
  });

  it("contains no duplicates", () => {
    const unique = new Set(IMAGE_PATHS);
    expect(unique.size).toBe(IMAGE_PATHS.length);
  });
});

describe("VALIDATION_TRIALS", () => {
  it("contains at least n_validation_trials entries", () => {
    expect(VALIDATION_TRIALS.length).toBeGreaterThanOrEqual(
      CONFIG.N_VALIDATION_TRIALS
    );
  });

  it("all trials have required fields", () => {
    for (const trial of VALIDATION_TRIALS) {
      expect(trial).toHaveProperty("type", "validation");
      expect(trial).toHaveProperty("stimulus");
      expect(trial).toHaveProperty("choice1");
      expect(trial).toHaveProperty("choice2");
    }
  });

  it("all stimulus paths reference images in IMAGE_PATHS", () => {
    const pathSet = new Set(IMAGE_PATHS);
    for (const trial of VALIDATION_TRIALS) {
      expect(pathSet.has(trial.stimulus)).toBe(true);
      expect(pathSet.has(trial.choice1)).toBe(true);
      expect(pathSet.has(trial.choice2)).toBe(true);
    }
  });

  it("no trial has duplicate images", () => {
    for (const trial of VALIDATION_TRIALS) {
      const images = [trial.stimulus, trial.choice1, trial.choice2];
      const unique = new Set(images);
      expect(unique.size).toBe(3);
    }
  });
});
