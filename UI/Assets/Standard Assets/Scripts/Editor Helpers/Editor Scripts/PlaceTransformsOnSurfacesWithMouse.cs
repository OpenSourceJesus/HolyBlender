#if UNITY_EDITOR
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Extensions;
using UnityEditor;

namespace HolyBlender
{
	[ExecuteInEditMode]
	public class PlaceTransformsOnSurfacesWithMouse : EditorScript
	{
		public Transform trs;
		public Transform paintParent;
		List<Vector3> previousPaintPositions = new List<Vector3>();
		Bounds goBounds;
		Bounds[] gosBounds = new Bounds[0];

		[MenuItem("Tools/Start placing objects on surfaces _F1")]
		static void _StartPlacing ()
		{
			FindObjectOfType<PlaceTransformsOnSurfacesWithMouse>().StartPlacing ();
		}

		[MenuItem("Tools/Stop placing objects on surfaces #F1")]
		static void _StopPlacing ()
		{
			FindObjectOfType<PlaceTransformsOnSurfacesWithMouse>().StopPlacing ();
		}

		public void StartPlacing ()
		{
			EditorApplication.update -= Paint;
			SceneView.duringSceneGui -= OnSceneGUI;
			previousPaintPositions.Clear();
			goBounds = trs.GetComponentInChildren<Renderer>().bounds;
			Collider[] colliders = FindObjectsOfType<Collider>();
			List<Bounds> _gosBounds = new List<Bounds>();
			for (int i = 0; i < colliders.Length; i ++)
			{
				Collider collider = colliders[i];
				Renderer renderer = collider.GetComponentInChildren<Renderer>();
				if (renderer != null)
					_gosBounds.Add(renderer.bounds);
			}
			gosBounds = _gosBounds.ToArray();
			SceneView.duringSceneGui += OnSceneGUI;
			EditorApplication.update += Paint;
		}

		void Paint ()
		{
			Ray mouseRay = GetMouseRay();
			List<Vector3> spawnPositions = new List<Vector3>();
			List<Quaternion> spawnRotations = new List<Quaternion>();
			for (int i = 0; i < gosBounds.Length; i ++)
			{
				Bounds bounds = gosBounds[i];
				Vector3 hit;
				if (bounds.Raycast(mouseRay, out hit))
				{
					Vector3 spawnPosition = new Vector3();
					Quaternion spawnRotation = new Quaternion();
					if (hit.x == bounds.min.x)
					{
						spawnPosition = new Vector3(hit.x - goBounds.extents.y, Mathf.Round(hit.y), Mathf.Round(hit.z));
						spawnRotation = Quaternion.LookRotation(Vector3.forward, Vector3.left);
					}
					else if (hit.x == bounds.max.x)
					{
						spawnPosition = new Vector3(hit.x + goBounds.extents.y, Mathf.Round(hit.y), Mathf.Round(hit.z));
						spawnRotation = Quaternion.LookRotation(Vector3.forward, Vector3.right);
					}
					else if (hit.y == bounds.min.y)
					{
						spawnPosition = new Vector3(Mathf.Round(hit.x), hit.y - goBounds.extents.y, Mathf.Round(hit.z));
						spawnRotation = Quaternion.LookRotation(Vector3.forward, Vector3.down);
					}
					else if (hit.y == bounds.max.y)
					{
						spawnPosition = new Vector3(Mathf.Round(hit.x), hit.y + goBounds.extents.y, Mathf.Round(hit.z));
						spawnRotation = Quaternion.LookRotation(Vector3.forward, Vector3.up);
					}
					else if (hit.z == bounds.min.z)
					{
						spawnPosition = new Vector3(Mathf.Round(hit.x), Mathf.Round(hit.y), hit.z - goBounds.extents.y);
						spawnRotation = Quaternion.LookRotation(Vector3.up, Vector3.back);
					}
					else
					{
						spawnPosition = new Vector3(Mathf.Round(hit.x), Mathf.Round(hit.y), hit.z + goBounds.extents.y);
						spawnRotation = Quaternion.LookRotation(Vector3.up, Vector3.forward);
					}
					spawnPositions.Add(spawnPosition);
					spawnRotations.Add(spawnRotation);
				}
			}
			int indexOfClosestSpawnPosition = VectorExtensions.GetIndexOfClosestPoint(mouseRay.origin, spawnPositions.ToArray());
			Vector3 _spawnPosition = spawnPositions[indexOfClosestSpawnPosition];
			if (!previousPaintPositions.Contains(_spawnPosition))
			{
				Quaternion spawnRotation = spawnRotations[indexOfClosestSpawnPosition];
				if (PrefabUtility.GetPrefabAssetType(trs) != PrefabAssetType.NotAPrefab)
				{
					Transform clonedTrs = (Transform) PrefabUtility.InstantiatePrefab(trs);
					clonedTrs.position = _spawnPosition;
					clonedTrs.rotation = spawnRotation;
					clonedTrs.SetParent(paintParent);
				}
				else
					Instantiate(trs, _spawnPosition, spawnRotation, paintParent);
				previousPaintPositions.Add(_spawnPosition);
			}
		}

		public void StopPlacing ()
		{
			EditorApplication.update -= Paint;
			SceneView.duringSceneGui -= OnSceneGUI;
		}

		void OnSceneGUI (SceneView sceneView)
		{
			UpdateHotkeys ();
		}

		public override void OnEnable ()
		{
			base.OnEnable ();
			StopPlacing ();
		}

		public override void OnDisable ()
		{
			base.OnDisable ();
			StopPlacing ();
		}

		public override void OnDestroy ()
		{
			base.OnDestroy ();
			StopPlacing ();
		}
	}
}
#else
namespace HolyBlender
{
	public class PlaceTransformsOnSurfacesWithMouse : EditorScript
	{
	}
}
#endif