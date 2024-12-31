#if UNITY_EDITOR
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;
using Extensions;
using UnityEditor;

namespace HolyBlender
{
	public class MakeGridOfTransformPrefabsInBounds : EditorScript
	{
		public Vector3 gridCellSize = Vector3.one;
		public BoundsOffset gridCellOffset = new BoundsOffset(Vector3.one / 2, Vector3.zero);
		public Transform trs;
		public Bounds bounds;

		public override void Do ()
		{
			if (trs == null)
				trs = GetComponent<Transform>();
			_Do (PrefabUtility.GetCorrespondingObjectFromSource(trs), bounds, gridCellSize, gridCellOffset, trs.parent);
		}

		public static Transform[] _Do (Transform trsPrefab, Bounds bounds, Vector3 gridCellSize, BoundsOffset gridCellOffset, Transform makeUnderParent = null)
		{
			List<Transform> output = new List<Transform>();
			Vector3[] pointsInside = bounds.GetPointsInside(gridCellSize, gridCellOffset);
			for (int i = 0; i < pointsInside.Length; i ++)
			{
				Vector3 pointInside = pointsInside[i];
				Transform trs = (Transform) PrefabUtility.InstantiatePrefab(trsPrefab);
				trs.SetParent(makeUnderParent);
				trs.position = pointInside;
				trs.SetWorldScale (gridCellSize);
				output.Add(trs);
			}
			return output.ToArray();
		}

		[MenuItem("Tools/Make grid of corresponding prefabs in selected mesh bounds")]
		static void _Do ()
		{
			Transform[] selectedTransforms = Selection.transforms;
			for (int i = 0; i < selectedTransforms.Length; i ++)
			{
				Transform selectedTrs = selectedTransforms[i];
				MeshFilter meshFilter = selectedTrs.GetComponent<MeshFilter>();
				if (meshFilter != null)
				{
					Bounds bounds = meshFilter.sharedMesh.bounds;
					bounds.center += selectedTrs.position;
					bounds.size = selectedTrs.rotation * bounds.size.Multiply(selectedTrs.lossyScale);
					_Do (PrefabUtility.GetCorrespondingObjectFromSource(selectedTrs), bounds, Vector3.one, new BoundsOffset(Vector3.one / 2, Vector3.zero), selectedTrs.parent);
				}
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class MakeGridOfTransformPrefabsInBounds : EditorScript
	{
	}
}
#endif