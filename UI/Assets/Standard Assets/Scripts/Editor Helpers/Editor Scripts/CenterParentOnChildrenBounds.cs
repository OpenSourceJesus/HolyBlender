#if UNITY_EDITOR
using Extensions;
using UnityEngine;
using UnityEditor;
using System.Collections;
using System.Collections.Generic;

namespace HolyBlender
{
	[ExecuteInEditMode]
	public class CenterParentOnChildrenBounds : EditorScript
	{
		public Transform trs;
		public bool useColliders;

		public override void Do ()
		{
			if (trs == null)
				trs = GetComponent<Transform>();
			_Do (trs, useColliders);
		}

		public static void _Do (Transform trs, bool useColliders)
		{
			Bounds bounds;
			if (useColliders)
			{
				Collider[] colliders = trs.GetComponentsInChildren<Collider>();
				Bounds[] collidersBounds = new Bounds[colliders.Length];
				for (int i = 0; i < colliders.Length; i ++)
				{
					Collider collider = colliders[i];
					collidersBounds[i] = collider.bounds;
				}
				bounds = collidersBounds.Combine();
			}
			else
			{
				Renderer[] renderers = trs.GetComponentsInChildren<Renderer>();
				Bounds[] renderersBounds = new Bounds[renderers.Length];
				for (int i = 0; i < renderers.Length; i ++)
				{
					Renderer renderer = renderers[i];
					renderersBounds[i] = renderer.bounds;
				}
				bounds = renderersBounds.Combine();
			}
			Vector3 previousPosition = trs.position;
			trs.position = bounds.center;
			Vector3 toPreviousPosition = previousPosition - trs.position;
			for (int i = 0; i < trs.childCount; i ++)
			{
				Transform child = trs.GetChild(i);
				child.position += toPreviousPosition;
			}
		}

		[MenuItem("Tools/Center selected parents on children colliders' bounds")]
		static void _DoForColliders ()
		{
			Transform[] selectedTransforms = Selection.transforms;
			for (int i = 0; i < selectedTransforms.Length; i ++)
			{
				Transform selectedTrs = selectedTransforms[i];
				_Do (selectedTrs, true);
			}
		}

		[MenuItem("Tools/Center selected parents on children renderers' bounds")]
		static void _DoForRenderers ()
		{
			Transform[] selectedTransforms = Selection.transforms;
			for (int i = 0; i < selectedTransforms.Length; i ++)
			{
				Transform selectedTrs = selectedTransforms[i];
				_Do (selectedTrs, false);
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class CenterParentOnChildrenBounds : EditorScript
	{
	}
}
#endif