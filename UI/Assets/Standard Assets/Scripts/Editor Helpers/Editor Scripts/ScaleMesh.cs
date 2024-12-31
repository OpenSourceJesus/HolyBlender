#if UNITY_EDITOR
using UnityEngine;
using Extensions;

namespace HolyBlender
{
	public class ScaleMesh : EditorScript
	{
		public MeshFilter meshFilter;
		public Vector3 scale;
		public bool useSharedMesh;

		public override void Do ()
		{
			if (meshFilter == null)
				meshFilter = GetComponent<MeshFilter>();
			Mesh mesh = meshFilter.mesh;
			if (useSharedMesh)
				mesh = meshFilter.sharedMesh;
			_Do (mesh, scale);
		}

		public static void _Do (Mesh mesh, Vector3 scale)
		{
			Vector3[] vertices = mesh.vertices;
			for (int i = 0; i < vertices.Length; i ++)
				vertices[i] = vertices[i].Multiply(scale);
			mesh.vertices = vertices;
		}
	}
}
#else
namespace HolyBlender
{
	public class ScaleMesh : EditorScript
	{
	}
}
#endif