module.exports = {
  rules: {
    // A temporary hack related to IDE not resolving correct package.json
    'import/no-extraneous-dependencies': 'off',
    // Since React 17 and typescript 4.1 you can safely disable the rule
    'react/react-in-jsx-scope': 'off',
    'prettier/prettier': 0,
    '@typescript-eslint/no-non-null-assertion': 0,
    'spaced-comment': 0, // downgrade to warning
    'react/prop-types': 0,
    'react/forbid-prop-types': 0,
    'jsx-a11y/anchor-is-valid': 0,
  }
}
