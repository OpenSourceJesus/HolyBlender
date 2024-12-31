using System;
using System.Collections.Generic;

[Serializable]
public class Graph<T>
{
	public List<Node> nodes = new List<Node>();

	public List<Node> GetConnectedGroup (Node node)
	{
		List<Node> output = new List<Node>();
		List<Node> checkedNodes = new List<Node>() { node };
		List<Node> remainingNodes = new List<Node>() { node };
		while (remainingNodes.Count > 0)
		{
			Node node2 = remainingNodes[0];
			output.Add(node2);
			for (int i = 0; i < node2.connectedTo.Count; i ++)
			{
				Node connectedNode = node2.connectedTo[i];
				if (!checkedNodes.Contains(connectedNode))
				{
					checkedNodes.Add(connectedNode);
					remainingNodes.Add(connectedNode);
				}
			}
			remainingNodes.RemoveAt(0);
		}
		return output;
	}

	public Node[] GetConnectedGroup_Array (Node node)
	{
		return GetConnectedGroup(node).ToArray();
	}

	public void RemoveNode (Node node, bool isBidirectionalGraph)
	{
		nodes.Remove(node);
		if (isBidirectionalGraph)
		{
			for (int i = 0; i < node.connectedTo.Count; i ++)
			{
				Node connectedNode = node.connectedTo[i];
				connectedNode.connectedTo.Remove(node);
			}
		}
		else
		{
			for (int i = 0; i < nodes.Count; i ++)
			{
				Node node2 = nodes[i];
				node2.connectedTo.Remove(node);
			}
		}
	}

	[Serializable]
	public struct Node
	{
		public T value;
		public List<Node> connectedTo;

		public Node (T value) : this (value, new List<Node>())
		{
		}

		public Node (T value, List<Node> connectedTo)
		{
			this.value = value;
			this.connectedTo = connectedTo;
		}
	}
}