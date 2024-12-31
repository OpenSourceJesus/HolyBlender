using UnityEngine;
using System.Collections.Generic;

namespace Extensions
{
	public static class LayerMaskExtensions
	{
		public static LayerMask Create (params string[] layerNames)
		{
			return FromLayerNames(layerNames);
		}
	 
		public static LayerMask Create (params int[] layerNumbers)
		{
			return FromLayerNumbers(layerNumbers);
		}
	 
		public static LayerMask FromLayerNames (params string[] layerNames)
		{
			LayerMask ret = (LayerMask) 0;
			foreach (string name in layerNames)
				ret |= (1 << LayerMask.NameToLayer(name));
			return ret;
		}
	 
		public static LayerMask FromLayerNumbers (params int[] layerNumbers)
		{
			LayerMask ret = (LayerMask) 0;
			foreach (int layer in layerNumbers)
				ret |= (1 << layer);
			return ret;
		}
	 
		public static LayerMask Inverse (this LayerMask original)
		{
			return ~original;
		}
	 
		public static LayerMask AddTo (this LayerMask original, params string[] layerNames)
		{
			foreach (string layerName in layerNames)
				original |= (1 << LayerMask.NameToLayer(layerName));
			return original;
		}
	 
		public static LayerMask AddTo (this LayerMask original, LayerMask layerMask)
		{
			return original.AddTo(layerMask.ToLayerNames());
		}
	 
		public static LayerMask Remove (this LayerMask original, params string[] layerNames)
		{
			LayerMask invertedOriginal = ~original;
			return ~(invertedOriginal | FromLayerNames(layerNames));
		}
	 
		public static string[] ToLayerNames (this LayerMask original)
		{
			List<string> output = new List<string>();
			for (int i = 0; i < 32; i ++)
			{
				int shifted = 1 << i;
				if ((original & shifted) == shifted)
				{
					string layerName = LayerMask.LayerToName(i);
					if (!string.IsNullOrEmpty(layerName))
						output.Add(layerName);
				}
			}
			return output.ToArray();
		}
	 
		public static string ToString (this LayerMask original)
		{
			return ToString(original, ", ");
		}
	 
		public static string ToString (this LayerMask original, string delimiter)
		{
			return string.Join(delimiter, ToLayerNames(original)) + delimiter;
		}
		
		public static bool Contains (this LayerMask original, int layer)
		{
			return original == (original | (1 << layer));
		}
	}
}