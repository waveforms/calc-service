import React, { useState, useEffect,  Fragment } from 'react';
//import logo from './logo.svg';
import './App.css';

import {JsonTreeView}from './JsonTreeView';
import { Map } from 'immutable'
import AddUserTreeForm from './addUserTree';

/* counter to keep track of unique ids.  Starts at 14 due to demo data. Will never decrease, only increase.*/
var idCounter = 5;
/* Map to help find a node parent in big-O O(1) time */
var parentMap = {1:0, 2:1,3:2,4:1};

/* this is demo data used to show the data structure */
const demo_data = {
  node_value_display: '1',
  id: 1,
  member_details: Map({  left_or_right:'root', number_children: '2', }),
  children: [
      {
          node_value_display: '2',
          id: 2,
          member_details: Map({  left_or_right:'left', number_children: '1', }),
          children: [
              { node_value_display: '5',
              id: 3,
              member_details: Map({  left_or_right:'right', number_children: '0', },),
              children: []
             }
          ]
      },
      {
          node_value_display: '3',
          id: 4,
          member_details: Map({ left_or_right:'right', number_children: '0', },),
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

function addChildToId(element, matchingId, node_value_display = '0',  left_or_right = 'left', number_children = '0'){
  idCounter++;
  var parent =  searchTreeById(element, parseInt(matchingId))
 
  var newChild = {
    node_value_display: node_value_display,
    id: idCounter,
    children: [],
    member_details: Map({  left_or_right: left_or_right, number_children: number_children, })
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

function App() {
  const [dataState, setDataState] = useState(demo_data);
  const [isLoading, setIsLoading] = useState(false);
  const [currentSum, setCurrentSum] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      const get_tree_url = window.calc_assets_url +"/" + window.calc_service_uid
      const res = await fetch(get_tree_url);
      const parsed = await res.json();
      
      if (parsed.data){
        setDataState(parsed.data);
      }
      setIsLoading(false);
    };
    fetchData();
  }, []);

  const handleValues = (values) => {
    addChildToId(dataState, values.parent_node_id, values.node_value_display,  values.left_or_right, values.number_children);
  };
  
  const onClickDN = () => {
    removeNodeById(dataState, idCounter)
  }

  const onClickSJ = () => {
    console.log("sending data")
    fetch(window.calc_assets_url + "/" +  window.calc_service_uid, {
        method: 'POST',
        mode: 'cors',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Access-Control-Allow-Credentials': 'true'
        },
        body: JSON.stringify(dataState)
      }).then(response => response.json())
        .then(data => {
          console.log(data.data.sum_lp);
          setCurrentSum(data.data.sum_lp)
        })
        .catch(function(err) {
        // Called if the server returns any errors
          console.log("Error:"+err);
        });
  }

  

  return (
   

   
    <div className="App">
      <div className="App-header"> 
      {isLoading ? (
        <div>Loading ...</div>
      ) : (
         <Fragment>
                <JsonTreeView data={dataState} shouldExpandNode={raw => true} />
                <p>Calc Sum Longest Path</p>
                <button onClick={()=>{onClickSJ()}}>Send to Calc Service</button>
                <p>Current Sum: {currentSum}</p>
                <p>Add a new Node</p>
                <AddUserTreeForm handleValues={handleValues} />
                {/* <p>Remove a Node</p>
                <button onClick={()=>{onClickDN()}}>Delete Node {idCounter}</button> */}
          </Fragment>


      )}

      </div>
    </div>
   
  );
}

export default App;
