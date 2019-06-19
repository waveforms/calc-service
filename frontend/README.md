# single-parent-tree
A single parent binary tree with unlimited depth.

The main data structure is a simple tree made up of javascript objects.
The size of the tree is only limited by the browser memory.

The application sends it's json structure to a server to calculate sum of the longest distance root to leaf.

Each family member can have an indefinite number of properties. Which is stored in the member_details map.

A new user will see a demo tree, which they can add nodes to.

Sending to the calc service will sum the longest path and also save the tree to the database.

The next time a logged in user loads the page, they will get their last saved tree.

# installation

built using node version v10.15.2
run `yarn` then `yarn start`

# testing
uses Jest and Enzyme
run 'yarn test`

# built with

#### Create React App
- because it is one of the quickest ways to build a react app

#### react-json-tree
- React JSON Viewer Component, Extracted from redux-devtools.

#### Formik and Yup
- one of the best ways to handle forms in jsx

#### immutable.js
- with immutable's `Map` application can dynamically add any number of properties to a user
