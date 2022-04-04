import React from 'react';

const Results = (props) => {
  console.log(props.names)
  return (
    props.names.map(row => 
      <div key={row.id}>
        {row.name}
      </div>
    )
  );
}

export default Results;