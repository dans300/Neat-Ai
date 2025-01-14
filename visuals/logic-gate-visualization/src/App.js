import React, { useState } from 'react';

const LogicGateVisualization = () => {
  // Sample historical data - in real implementation this would come from your game
  const [stateHistory] = useState([
    {
      matrix: [[0,1,0], [1,1,0], [0,1,1]],
      commands: ["UP", "ATTACK"]
    },
    {
      matrix: [[1,0,0], [1,1,0], [0,1,0]],
      commands: ["DOWN", "EAT"]
    }
  ]);

  const getMatrixOnes = (matrix) => {
    const ones = [];
    matrix.forEach((row, rowIdx) => {
      row.forEach((cell, colIdx) => {
        if (cell === 1) {
          ones.push({ row: rowIdx, col: colIdx });
        }
      });
    });
    return ones;
  };

  return (
    <div className="w-full h-screen bg-gray-900 p-4 overflow-auto">
      {stateHistory.map((state, stateIdx) => (
        <div key={stateIdx} className="mb-20 relative">
          {/* Matrix Display */}
          <div className="absolute left-4 top-0">
            {state.matrix.map((row, rowIdx) => (
              <div key={rowIdx} className="flex">
                {row.map((cell, colIdx) => (
                  <div
                    key={`${rowIdx}-${colIdx}`}
                    className={`w-8 h-8 border border-gray-600 flex items-center justify-center m-0.5
                      ${cell === 1 ? 'bg-blue-500' : 'bg-gray-800'} text-white`}
                  >
                    {cell}
                  </div>
                ))}
              </div>
            ))}
          </div>

          {/* AND Gate SVG */}
          <svg className="absolute left-40 w-[calc(100%-160px)] h-40">
            {/* AND Gate Symbol */}
            <path
              d="M 100,10 L 100,50 Q 130,30 100,10"
              fill="none"
              stroke="white"
              strokeWidth="2"
            />

            {/* Input Lines */}
            {getMatrixOnes(state.matrix).map((one, idx) => {
              const yOffset = 10 + (idx * 15);
              return (
                <path
                  key={idx}
                  d={`M 0,${yOffset} L 100,${yOffset}`}
                  stroke="white"
                  strokeWidth="2"
                />
              );
            })}

            {/* Output Line */}
            <path
              d="M 130,30 L 180,30"
              stroke="white"
              strokeWidth="2"
            />

            {/* Commands */}
            <g transform="translate(200, 0)">
              {state.commands.map((cmd, idx) => (
                <g key={idx}>
                  <rect
                    x="0"
                    y={idx * 40}
                    width="80"
                    height="30"
                    fill="#4A5568"
                    rx="4"
                  />
                  <text
                    x="40"
                    y={idx * 40 + 20}
                    textAnchor="middle"
                    fill="white"
                    className="text-sm"
                  >
                    {cmd}
                  </text>
                  {/* Lines from AND gate output to each command */}
                  <path
                    d={`M -20,30 L -10,${idx * 40 + 15}`}
                    stroke="white"
                    strokeWidth="2"
                  />
                </g>
              ))}
            </g>
          </svg>
        </div>
      ))}
    </div>
  );
};

export default LogicGateVisualization;
