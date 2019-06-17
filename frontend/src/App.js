import React from 'react';
//import logo from './logo.svg';
import './App.css';

//import {TreeExample}from './TreeExample';
import {JsonTreeView}from './JsonTreeView';
import { Map } from 'immutable'
import AddUserTreeForm from './addUserTree';

/* counter to keep track of unique ids.  Starts at 14 due to demo data. Will never decrease, only increase.*/
var idCounter = 5;
/* Map to help find a node parent in big-O O(1) time */
var parentMap = {1:0, 2:1,3:2,4:1};

/* this is demo data used to show the data structure */
const data = {
  node_value_display: '1',
  id: 1,
  member_details: Map({ node_value: '1', left_or_right:'root', number_children: '2', }),
  children: [
      {
          node_value_display: '2',
          id: 2,
          member_details: Map({ node_value: '2', left_or_right:'left', number_children: '1', }),
          children: [
              { node_value_display: '5',
              id: 3,
              member_details: Map({ node_value: '2', left_or_right:'right', number_children: '0', },),
              children: []
             }
          ]
      },
      {
          node_value_display: '3',
          id: 4,
          member_details: Map({ node_value: '3', left_or_right:'right', number_children: '0', },),
          children: []
      }
    ]}
      

function searchTreeById(element, matchingId){
  if(element.id === matchingId){
       return element;
  }else if (element.children != null){
       var i;
       var result = null;
       for(i=0; result == null && i < element.children.length; i++){
            result = searchTreeById(element.children[i], matchingId);
       }
       return result;
  }
  return null;
}

function addChildToId(element, matchingId, node_value_display = '0', node_value = '0', left_or_right = 'left', number_children = '0'){
  idCounter++;
  var parent =  searchTreeById(element, parseInt(matchingId))
 
  var newChild = {
    node_value_display: node_value_display,
    id: idCounter,
    member_details: Map({ node_value: node_value, left_or_right: left_or_right, number_children: number_children, })
  }
  
  if(parent.children == null){
    //add children array
    parent.children = []
  }
  if (parent.children.length < 2){
    parent.children.push(newChild)
    parent.member_details.set('number_children',parent.children.length);
    //update parentMap
    var pair = {};
    pair[idCounter] = parent.id;
    parentMap = {...parentMap, ...pair}; 
  }
  else {
    console.log("find another node")
  }
  
  
  return null;
}

function removeNodeById(element, matchingId){
   let parentid = parentMap[matchingId];
   if (parentid == null){
     return null
   }
   let parent = searchTreeById(element, parentid);
   if (parent.children.length === 1){
     
     delete parent.children
   }
   else {
    parent.children = parent.children.filter(function(el) { return el.id !== matchingId; }); 

   }
   //update parentMap
   delete parentMap[matchingId]

}

const handleValues = (values) => {
  addChildToId(data, values.parent_node_id, values.node_value_display, values.node_value, values.left_or_right, values.number_children);
};

const onClickDN = () => {
  removeNodeById(data, idCounter)
}

const onClickSJ = () => {
  console.log("sending data")
  fetch(window.calc_assets_url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => {
        console.log(data.data.sum_lp);
        alert(data.data.sum_lp)
      })
      .catch(function(err) {
      // Called if the server returns any errors
        console.log("Error:"+err);
      });
}




var data_subsection = searchTreeById(data, 1);


function App() {
  return (
    <div className="App">
      <header className="App-header">
      <JsonTreeView data={data_subsection} shouldExpandNode={raw => true} />
      <p>Calc Sum Longest Path</p>
      <button onClick={()=>{onClickSJ()}}>Send to Calc Service</button>
      <p>Add a new Node</p>
      <AddUserTreeForm handleValues={handleValues} />
      <p>Remove a Node</p>
      <button onClick={()=>{onClickDN()}}>Delete Node {idCounter}</button>
      
      </header>
    </div>
  );
}

export default App;
