using System;
using Extensions;
using UnityEngine;
using System.Collections.Generic;

[Serializable]
public struct SpatialHashGrid2D<T>
{
	public Rect rect;
	public float cellSize;
	public Vector2 cellOffset;
	public List<Agent>[,] agents;

	public SpatialHashGrid2D (float cellSize, Vector2Int cellCount, Vector2 minCellPosition)
	{
		Vector2 rectSize = cellCount.ToVec2() * cellSize;
		rect = new Rect(minCellPosition + rectSize / 2, rectSize);
		this.cellSize = cellSize;
		cellOffset = minCellPosition + Vector2.one * cellSize / 2;
		agents = new List<Agent>[cellCount.x, cellCount.y];
		Init ();
	}

	public SpatialHashGrid2D (Rect rect, float cellSize)
	{
		this.rect = rect;
		this.cellSize = cellSize;
		Vector2Int cellCount = new Vector2Int((int) Mathf.Ceil(rect.size.x / cellSize), (int) Mathf.Ceil(rect.size.y / cellSize));
		Vector2 minCellPosition = rect.min - (cellCount - rect.size / cellSize) / 2;
		cellOffset = minCellPosition + Vector2.one * cellSize / 2;
		agents = new List<Agent>[cellCount.x, cellCount.y];
		Init ();
	}

	public void Init ()
	{
		for (int x = 0; x < agents.GetLength(0); x ++)
		{
			for (int y = 0; y < agents.GetLength(1); y ++)
				agents[x, y] = new List<Agent>();
		}
	}

	public Vector2Int Evaluate (Vector2 position)
	{
		return ((position - cellOffset) / cellSize).ToVec2Int();
	}

	public Agent[] GetClosebyAgents (Vector2 position)
	{
		return GetClosebyAgents(Evaluate(position));
	}

	public Agent[] GetClosebyAgents (Vector2Int cellPosition)
	{
		List<Agent> output = new List<Agent>(agents[cellPosition.x, cellPosition.y]);
		output.AddRange(agents[cellPosition.x - 1, cellPosition.y - 1]);
		output.AddRange(agents[cellPosition.x - 1, cellPosition.y]);
		output.AddRange(agents[cellPosition.x, cellPosition.y - 1]);
		output.AddRange(agents[cellPosition.x + 1, cellPosition.y + 1]);
		output.AddRange(agents[cellPosition.x + 1, cellPosition.y]);
		output.AddRange(agents[cellPosition.x, cellPosition.y + 1]);
		output.AddRange(agents[cellPosition.x - 1, cellPosition.y + 1]);
		output.AddRange(agents[cellPosition.x + 1, cellPosition.y - 1]);
		return output.ToArray();
	}

	[Serializable]
	public struct Agent
	{
		public Vector2 position;
		public Vector2Int cellPosition;
		public T value;
		public SpatialHashGrid2D<T> spatialHashGrid;

		public Agent (Vector2 position, T value, SpatialHashGrid2D<T> spatialHashGrid)
		{
			this.position = position;
			cellPosition = spatialHashGrid.Evaluate(position);
			this.value = value;
			this.spatialHashGrid = spatialHashGrid;
			spatialHashGrid.agents[cellPosition.x, cellPosition.y].Add(this);
		}

		public void Remove ()
		{
			spatialHashGrid.agents[cellPosition.x, cellPosition.y].Remove(this);
		}

		public void Update (Vector2 position)
		{
			Remove ();
			this.position = position;
			cellPosition = spatialHashGrid.Evaluate(position);
			spatialHashGrid.agents[cellPosition.x, cellPosition.y].Add(this);
		}
	}
}