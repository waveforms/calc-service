import React from 'react';
import JSONTree from 'react-json-tree';

export const JsonTreeView = (props) => {
    
    return (
        <JSONTree data={props.data} />
    )
}