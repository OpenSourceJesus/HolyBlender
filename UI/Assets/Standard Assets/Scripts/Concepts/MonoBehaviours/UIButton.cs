using Extensions;
using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;

namespace HolyBlender
{
	public class UIButton : Button, IUpdatable
	{
		public Transform trs;
		public Image image;
		public GameObject goWhenPressed;

		void OnEnable ()
		{
			GameManager.updatables = GameManager.updatables.Add(this);
		}

		public void DoUpdate ()
		{
			if (!interactable)
				return;
			if (IsPressed())
			{
				goWhenPressed.SetActive(true);
				image.color = image.color.SetAlpha(0);
			}
			else
			{
				goWhenPressed.SetActive(false);
				image.color = image.color.SetAlpha(1);
			}
		}

		void OnDisable ()
		{
			GameManager.updatables = GameManager.updatables.Remove(this);
		}
	}
}