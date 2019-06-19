import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { demo_data } from './DemoData';
import {JsonTreeView}from './JsonTreeView';
import AddUserTreeForm from './addUserTree';
import { Map } from 'immutable'
import { configure, shallow, mount, render} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);
});

it('renders without crashing', () => {
  shallow(<JsonTreeView data={eval(demo_data)} />);
});

it('renders without crashing', () => {
  shallow(<AddUserTreeForm />);
});
