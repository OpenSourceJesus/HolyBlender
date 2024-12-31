using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Extensions;
using UnityEngine.Events;

[RequireComponent(typeof(Selectable))]
[ExecuteInEditMode]
public class _Selectable : MonoBehaviour
{
	public RectTransform rectTrs;
	public Selectable selectable;
	public UnityEvent onSelected;
	public UnityEvent onDeselected;
	public static _Selectable[] instances = new _Selectable[0];

	void OnEnable ()
	{
#if UNITY_EDITOR
		if (!Application.isPlaying)
		{
			if (rectTrs == null)
				rectTrs = GetComponent<RectTransform>();
			if (selectable == null)
				selectable = GetComponent<Selectable>();
			return;
		}
#endif
		instances = instances.Add(this);
	}

	void OnDisable ()
	{
#if UNITY_EDITOR
		if (!Application.isPlaying)
			return;
#endif
		instances = instances.Remove(this);
	}
}
