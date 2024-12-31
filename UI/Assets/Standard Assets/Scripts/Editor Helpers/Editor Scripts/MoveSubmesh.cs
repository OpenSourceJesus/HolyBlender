#if UNITY_EDITOR
using UnityEngine;
using System.Collections.Generic;

namespace HolyBlender
{
	public class MoveSubmesh : EditorScript
	{
		public MeshFilter meshFilter;
		public int submeshIndex;
		public Vector3 move;
		public bool useSharedMesh;

		public override void Do ()
		{
			if (meshFilter == null)
				meshFilter = GetComponent<MeshFilter>();
			Mesh mesh = meshFilter.mesh;
			if (useSharedMesh)
				mesh = meshFilter.sharedMesh;
			_Do (mesh, move, submeshIndex);
		}

		public static void _Do (Mesh mesh, Vector3 move, int submeshIndex)
		{
			Vector3[] vertices = mesh.vertices;
			List<int> triangles = new List<int>();
			mesh.GetTriangles(triangles, submeshIndex);
			for (int i = 0; i < vertices.Length; i ++)
			{
				if (triangles.Contains(i))
					vertices[i] += move;
			}
			mesh.vertices = vertices;
		}
	}
}
#else
namespace HolyBlender
{
	public class MoveSubmesh : EditorScript
	{
	}
}
#endif