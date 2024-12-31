#if UNITY_EDITOR
using Extensions;
using UnityEngine;
using UnityEditor;
using UnityEngine.Tilemaps;

namespace HolyBlender
{
	public class MakeCollider2DMeshAsset : MakeMeshAsset
	{
		public Collider2D collider;

		public override void Do ()
		{
			if (useSharedMesh)
				meshFilter.sharedMesh = collider.CreateMesh(true, true);
			else
				meshFilter.mesh = collider.CreateMesh(true, true);
			base.Do ();
		}
	}
}
#else
namespace HolyBlender
{
	public class MakeCollider2DMeshAsset : MakeMeshAsset
	{
	}
}
#endif