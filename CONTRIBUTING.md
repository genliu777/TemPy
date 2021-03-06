## Tempy | Contibution program and guidelines

### Guidelines
Any contribution is welcomed, fork and PR if you have some ideas you want to code in, I'll check them out.
Please write your own tests, no merge will be made without the relative tests.

PM me if you want to help maintaining this project or if you are willing to develop some of the next goals.

Open an Issue to ask for features, suggest ideas, or report a bug.

We have a [Slack](https://tempy-dev.slack.com) for TemPy dev discussions (ask for an invitation at federicocerchiari @ gmail . com).

### Program
Planned evolution of this project:
- Better exception handling.
- Manage Tempy object subclassing to use a custom object as a renderable for businnes logic item (i.e: SQLAlchemy's declarative with a Tempy template in it that can be rendered at ease)
- TemPy widgets, see the widget branch.
- Make pretty formatting of the output html.
- Writing more tests.

Ideas I'm thinking about:
- Html to TemPy command line converter tool, accepts plain html and makes a .py tempy module.
- Python 2 compatibility (maybe?).
- Performance: always needed, maybe a `_partial_render` method that traverse the html tree in a depth-first reverse order and "stabilize" all the leafs? Is this useful?
- Adding .find method to use with css-like selectors (i.e: `Html().find('#myid')`)?
- New class: `CssManager` extracts common style properties from the DOM, creates the `Css` instance and adds it in the `<head>`?
- Cache for css builder module in a separate script (i.e: `shell >>> tempy -build_css my_template.py` outputs a css in the static folder and the `CssManager` search for that version in the statics before doing any work)?
- Any suggestion?
