import React, { Component } from 'react';
import './App.css';
import Immutable, { List, Map } from 'immutable';

class App extends Component {
  constructor (props) {
    super(props);

    let row = new Array(20);
    row.fill(50);
    let world = new Array(20);
    world.fill(row);
    console.log(world);


    this.state = {
      rect: Immutable.fromJS(world)
    };
  }
  render() {
    let pixelSize = 40;

    let screen = this.state.rect.map((row) => row.map((cell) => Math.random() * 20));

    return (
      <div className="App">
        <div className="App-header">
          <h2>Welcome to React</h2>
        </div>
        <svg height={screen.size * pixelSize} width={screen.first().size * pixelSize}>
          {screen.map((row, y) => <g key={y}>
            {row.map((colorNum, x) => {
              let color = rgbToHex(colorNum, colorNum, colorNum);
              return <g key={x} >
                <rect x={pixelSize * x} y={pixelSize * y} fill={color} width={pixelSize} height={pixelSize} />
                <text x={pixelSize * x} y={pixelSize * (y + 0.5)}>{Math.round(colorNum)}</text>
              </g>
            })}
          </g>)}
        </svg>
      </div>
    );
  }
}

export default App;

function componentToHex(c) {
  let hex = Math.round(c).toString(16);
  return hex.length === 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}