#How To Contribute


Every open source project lives due to generous help by contributors sacrificing their time; arctic is no different.

Here are a few guidelines to get you started:

- Try to limit each pull request to one change only.
- To run the test suite, all you need is a recent [`tox`][1].
  It will ensure the test suite runs with all dependencies against all Python versions just as it will on [`Travis CI`][2].
  If you lack some Python versions, you can can always limit the environments like `tox -e py27,py35`.
- Make sure your changes pass our CI.
  You won't get any feedback until it's green unless you ask for it.
- If your change is noteworthy, add an entry to the CHANGELOG.
  Use present tense, semantic newlines, and add a link to your pull request.
- No contribution is too small; please submit as many fixes for typos and grammar bloopers as you can!
- Add yourself to AUTHORS if you have contributed and your name is not there yet.
- Don’t break backward compatibility.
- **Always** add tests and docs for your code.
  This is a hard rule; patches with missing tests or documentation won’t be merged.
- Obey [PEP 8][4].
- If you address review feedback, make sure to bump the pull request.
  Maintainers don’t receive notifications when you push new commits.

Thank you for considering contributing to arctic!


[1]: https://testrun.org/tox/
[2]: https://travis-ci.org/
[4]: https://www.python.org/dev/peps/pep-0008/

*Based on:* <https://github.com/hynek/attrs/blob/master/CONTRIBUTING.rst>