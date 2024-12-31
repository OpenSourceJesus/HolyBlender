using System.Collections;
using System.Collections.Generic;
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif

namespace Extensions
{
	public static class TransformExtensions
	{
		public static Transform FindChild (this Transform trs, string childName)
		{
			List<Transform> remainingChildren = new List<Transform>();
			remainingChildren.Add(trs);
			while (remainingChildren.Count > 0)
			{
				foreach (Transform child in remainingChildren[0])
				{
					if (child.name.Equals(childName))
						return child;
					remainingChildren.Add(child);
				}
				remainingChildren.RemoveAt(0);
			}
			return null;
		}

		public static Transform[] FindChildren (this Transform trs, string childName)
		{
			List<Transform> output = new List<Transform>();
			List<Transform> remainingChildren = new List<Transform>();
			remainingChildren.Add(trs);
			while (remainingChildren.Count > 0)
			{
				foreach (Transform child in remainingChildren[0])
				{
					if (child.name.Equals(childName))
						output.Add(child);
					remainingChildren.Add(child);
				}
				remainingChildren.RemoveAt(0);
			}
			return output.ToArray();
		}

		public static Transform FindClosestTransform (Transform[] transforms, Transform closestTo)
		{
			while (transforms.Contains(null))
				transforms = transforms.Remove(null);
			if (transforms.Length == 0)
				return null;
			else if (transforms.Length == 1)
				return transforms[0];
			int closestOpponentIndex = 0;
			for (int i = 1; i < transforms.Length; i ++)
			{
				Transform checkOpponent = transforms[i];
				Transform currentClosestOpponent = transforms[closestOpponentIndex];
				if (Vector2.Distance(closestTo.position, checkOpponent.position) < Vector2.Distance(closestTo.position, currentClosestOpponent.position))
					closestOpponentIndex = i;
			}
			return transforms[closestOpponentIndex];
		}

		public static Transform GetClosestTransform_2D (this Transform trs, Transform[] transforms)
		{
			Transform closestTrs = transforms[0];
			float closestDistance = ((Vector2) (trs.position - closestTrs.position)).sqrMagnitude;
			for (int i = 1; i < transforms.Length; i ++)
			{
				Transform transform = transforms[i];
				float distance = ((Vector2) (trs.position - closestTrs.position)).sqrMagnitude;
				if (distance < closestDistance)
				{
					closestTrs = trs;
					closestDistance = distance;
				}
			}
			return closestTrs;
		}

		public static Transform GetClosestTransform_2D (this Transform[] transforms, Vector2 position)
		{
			Transform closestTrs = transforms[0];
			float closestDistance = (position - (Vector2) closestTrs.position).sqrMagnitude;
			for (int i = 1; i < transforms.Length; i ++)
			{
				Transform trs = transforms[i];
				float distance = (position - (Vector2) trs.position).sqrMagnitude;
				if (distance < closestDistance)
				{
					closestTrs = trs;
					closestDistance = distance;
				}
			}
			return closestTrs;
		}

		public static Transform GetClosestTransform_3D (this Transform trs, Transform[] transforms)
		{
			Transform closestTrs = transforms[0];
			float closestDistance = (trs.position - closestTrs.position).sqrMagnitude;
			for (int i = 1; i < transforms.Length; i ++)
			{
				Transform transform = transforms[i];
				float distance = (trs.position - closestTrs.position).sqrMagnitude;
				if (distance < closestDistance)
				{
					closestTrs = trs;
					closestDistance = distance;
				}
			}
			return closestTrs;
		}

		public static Transform GetClosestTransform_3D (this Transform[] transforms, Vector3 position)
		{
			Transform closestTrs = transforms[0];
			float closestDistance = (position - closestTrs.position).sqrMagnitude;
			for (int i = 1; i < transforms.Length; i ++)
			{
				Transform trs = transforms[i];
				float distance = (position - trs.position).sqrMagnitude;
				if (distance < closestDistance)
				{
					closestTrs = trs;
					closestDistance = distance;
				}
			}
			return closestTrs;
		}

		public static Rect GetRect (this Transform trs)
		{
			return Rect.MinMaxRect(trs.position.x - trs.lossyScale.x / 2, trs.position.y - trs.lossyScale.y / 2, trs.position.x + trs.lossyScale.x / 2, trs.position.y + trs.lossyScale.y / 2);
		}

		public static Bounds GetBounds (this Transform trs)
		{
			return new Bounds(trs.position, trs.rotation * trs.lossyScale);
		}

		public static bool IsSameOrientationAndScale (this Transform trs, Transform other)
		{
			return trs.position == other.position && trs.rotation == other.rotation && trs.lossyScale == other.lossyScale;
		}

		public static Transform FindEquivalentChild (Transform root1, Transform child1, Transform root2)
		{
			TreeNode<Transform> childTree1 = root1.GetChildTree();
			int[] pathToChild1 = childTree1.GetPathToChild(child1);
			TreeNode<Transform> childTree2 = root2.GetChildTree().GetChildAtPath(pathToChild1);
			return childTree2.Value;
		}

		public static TreeNode<Transform> GetChildTree (this Transform root)
		{
			TreeNode<Transform> output = new TreeNode<Transform>(root);
			List<Transform> remainingChildren = new List<Transform>();
			remainingChildren.Add(root);
			Transform currentTrs;
			while (remainingChildren.Count > 0)
			{
				currentTrs = remainingChildren[0];
				foreach (Transform child in currentTrs)
				{
					output.GetRoot().GetChild(currentTrs).AddChild(child);
					remainingChildren.Add(child);
				}
				remainingChildren.RemoveAt(0);
			}
			return output;
		}

		public static void SetWorldScale (this Transform trs, Vector3 scale)
		{
			trs.localScale = Vector3.one;
			trs.localScale = scale.Divide(trs.lossyScale);
		}

		public static Matrix4x4 GetMatrix (this Transform trs)
		{
			return Matrix4x4.TRS(trs.position, trs.rotation, trs.lossyScale);
		}

		public static Transform InsertParent (this Transform trs)
		{
			Transform parent = new GameObject().GetComponent<Transform>();
			parent.SetParent(trs.parent);
			trs.SetParent(parent);
			return parent;
		}

		public static Transform[] GetAllChildren (this Transform trs)
		{
			List<Transform> output = new List<Transform>();
			List<Transform> remainingChildren = new List<Transform>();
			remainingChildren.Add(trs);
			while (remainingChildren.Count > 0)
			{
				foreach (Transform child in remainingChildren[0])
				{
					remainingChildren.Add(child);
					output.Add(child);
				}
				remainingChildren.RemoveAt(0);
			}
			return output.ToArray();
		}

#if UNITY_EDITOR
		public static Transform InsertParentAndRegisterUndo (this Transform trs)
		{
			Transform parent = new GameObject().GetComponent<Transform>();
			Undo.RegisterCreatedObjectUndo(parent.gameObject, "Insert parent");
			parent.SetParent(trs.parent);
			Undo.SetTransformParent(trs, parent, "Insert parent");
			return parent;
		}
#endif
	}
}