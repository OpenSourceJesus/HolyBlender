#if UNITY_EDITOR
using UnityEngine;

namespace HolyBlender
{
	public class RotateMesh : EditorScript
	{
		public MeshFilter meshFilter;
		public Vector3 rotation;
		public bool useSharedMesh;

		public override void Do ()
		{
			if (meshFilter == null)
				meshFilter = GetComponent<MeshFilter>();
			Mesh mesh = meshFilter.mesh;
			if (useSharedMesh)
				mesh = meshFilter.sharedMesh;
			_Do (mesh, rotation);
		}

		public static void _Do (Mesh mesh, Vector3 rotation)
		{
			Vector3[] vertices = mesh.vertices;
			for (int i = 0; i < vertices.Length; i ++)
				vertices[i] = Quaternion.Euler(rotation) * vertices[i];
			mesh.vertices = vertices;
		}
	}
}
#else
namespace HolyBlender
{
	public class RotateMesh : EditorScript
	{
	}
}
#endif