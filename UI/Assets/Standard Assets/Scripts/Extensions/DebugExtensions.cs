using System;
using HolyBlender;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class DebugExtensions
	{
		public static void DrawPoint (Vector3 point, float radius, Color color, float duration, Quaternion rotation = default(Quaternion))
		{
			Debug.DrawLine(point + rotation * (Vector3.right * radius), point + rotation * (Vector3.left * radius), color, duration);
			Debug.DrawLine(point + rotation * (Vector3.up * radius), point + rotation * (Vector3.down * radius), color, duration);
			Debug.DrawLine(point + rotation * (Vector3.forward * radius), point + rotation * (Vector3.back * radius), color, duration);
		}

		public static void DrawRect (Rect rect, Color color, float duration, Quaternion rotation = default(Quaternion))
		{
			Debug.DrawLine(rotation * rect.min, rotation * new Vector2(rect.xMin, rect.yMax), color, duration);
			Debug.DrawLine(rotation * new Vector2(rect.xMin, rect.yMax), rotation * rect.max, color, duration);
			Debug.DrawLine(rotation * rect.max, rotation * new Vector2(rect.xMax, rect.yMin), color, duration);
			Debug.DrawLine(rotation * new Vector2(rect.xMax, rect.yMin), rotation * rect.min, color, duration);
		}

		public static void DrawBounds (Bounds bounds, Color color, float duration, Quaternion rotation = default(Quaternion))
		{
			LineSegment3D[] sides = bounds.GetSides();
			for (int i = 0; i < sides.Length; i ++)
			{
				LineSegment3D side = sides[i];
				Debug.DrawLine(rotation * side.start, rotation * side.end, color, duration);
			}
		}

		public static void Log (string elementSeperator = ", ", LogType logType = LogType.Info, params object[] data)
		{
			if (logType == LogType.Info)
				Debug.Log(data.ToString(elementSeperator));
			else if (logType == LogType.Warning)
				Debug.LogWarning(data.ToString(elementSeperator));
			else//if (logType == LogType.Error)
				Debug.LogError(data.ToString(elementSeperator));
		}

		public static void Log (in object data, LogType logType = LogType.Info)
		{
			if (logType == LogType.Info)
				Debug.Log(data.ToString());
			else if (logType == LogType.Warning)
				Debug.LogWarning(data.ToString());
			else//if (logType == LogType.Error)
				Debug.LogError(data.ToString());
		}

		public static void DelayedLog (float delay, bool realtime = true, string elementSeperator = ", ", LogType logType = LogType.Info, params object[] data)
		{
			GameManager.Instance.StartCoroutine(DelayedLogRoutine (delay, realtime, elementSeperator, logType, data));
		}

		public static IEnumerator DelayedLogRoutine (float delay, bool realtime = true, string elementSeperator = ", ", LogType logType = LogType.Info, params object[] data)
		{
			if (realtime)
				yield return new WaitForSecondsRealtime(delay);
			else
				yield return new WaitForSeconds(delay);
			Log (elementSeperator, logType, data);
		}

		public enum LogType
		{
			Info,
			Error,
			Warning
		}
	}
}