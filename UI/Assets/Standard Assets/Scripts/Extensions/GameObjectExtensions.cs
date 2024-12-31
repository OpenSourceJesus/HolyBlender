using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

namespace Extensions
{
	public static class GameObjectExtensions
	{
		public static GameObject FindWithComponentInParents (Transform child, string componentName)
		{
			while (child != null)
			{
				child = child.parent;
				if (child != null)
				{
					if (child.GetComponent(componentName) != null)
						return child.gameObject;
				}
			}
			return null;
		}
		
		public static GameObject FindWithComponentInParents (Transform child, Type componentType)
		{
			return FindWithComponentInParents (child, componentType.Name);
		}
	}
}