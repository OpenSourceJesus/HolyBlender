#if UNITY_EDITOR
using Extensions;
using UnityEditor;
using UnityEngine;
using System.Collections.Generic;

namespace HolyBlender
{
	[ExecuteInEditMode]
	public class HandleOnlyActiveInViews : EditorScript
	{
		// public bool update;
		// public SpatialHashGrid2D<OnlyActiveInView> spatialHashGrid;
		// public Rect rect;
		// public float cellSize;
		// public List<SpatialHashGrid2D<OnlyActiveInView>.Agent> agents = new List<SpatialHashGrid2D<OnlyActiveInView>.Agent>();
		public float multiplyViewSize;
		[HideInInspector]
		public bool previousDoRepeatedly;

		public override void OnValidate ()
		{
			base.OnValidate ();
			if (!doRepeatedly && previousDoRepeatedly)
			{
				for (int i = 0; i < OnlyActiveInView.instances.Count; i ++)
				{
					OnlyActiveInView onlyActiveInView = OnlyActiveInView.instances[i];
					if (onlyActiveInView.enabled)
						onlyActiveInView.gameObject.SetActive(true);
				}
			}
			previousDoRepeatedly = doRepeatedly;
			// if (update)
			// {
			// 	update = false;
			// 	_Update ();
			// }
		}

		public override void Do ()
		{
			Camera camera = GetSceneViewCamera();
			Vector2 viewSize = new Vector2(camera.orthographicSize / 2 * camera.aspect, camera.orthographicSize / 2) * multiplyViewSize;
			Rect viewRect = new Rect((Vector2) camera.transform.position - viewSize / 2, viewSize);
			for (int i = 0; i < OnlyActiveInView.instances.Count; i ++)
			{
				OnlyActiveInView onlyActiveInView = OnlyActiveInView.instances[i];
				if (onlyActiveInView.enabled)
				{
					bool activate = viewRect.Contains(onlyActiveInView.trs.position);
					if (!activate)
					{
						Transform[] allChildren = onlyActiveInView.trs.GetAllChildren();
						for (int i2 = 0; i2 < allChildren.Length; i2 ++)
						{
							Transform child = allChildren[i2];
							if (viewRect.Contains(child.position))
							{
								activate = true;
								break;
							}
						}
					}
					onlyActiveInView.gameObject.SetActive(activate);
				}
			}
		}

		// void _Update ()
		// {
		// 	spatialHashGrid = new SpatialHashGrid2D<OnlyActiveInView>(rect, cellSize);
		// 	agents.Clear();
		// 	for (int i = 0; i < OnlyActiveInView.instances.Count; i ++)
		// 	{
		// 		OnlyActiveInView onlyActiveInView = OnlyActiveInView.instances[i];
		// 		agents.Add(new SpatialHashGrid2D<OnlyActiveInView>.Agent(onlyActiveInView.trs.position, onlyActiveInView, spatialHashGrid));
		// 	}
		// }
	}
}
#else
namespace HolyBlender
{
	public class HandleOnlyActiveInViews : EditorScript
	{
	}
}
#endif