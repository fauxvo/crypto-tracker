"use strict";

module.exports = {
  root: true,
  extends: [
    "plugin:@typescript-eslint/recommended",
    "plugin:prettier/recommended",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: "module",
  },
  env: { node: true },
  rules: {
    // TODO: Enable these rules one by one
    "@typescript-eslint/no-explicit-any": 0,
    "@typescript-eslint/explicit-module-boundary-types": 0,
    "@typescript-eslint/no-non-null-assertion": 0,
    "@typescript-eslint/ban-types": 0,
    "@typescript-eslint/no-var-requires": 0,
  },
  overrides: [
    {
      files: ["src/**/*.js", ".eslintrc.js", "jest.config.js"],
      parser: "esprima",
      parserOptions: { sourceType: "script" },
      rules: {
        strict: [2, "global"],
      },
    },
    {
      files: ["src/tests/**/*.test.ts"],
      plugins: ["jest"],
      env: { jest: true },
    },
  ],
};
