/*
	This file defines a TMP_Text that can be temporarily and locally activated for a duration defined by 'durationPerCharacter * [the number of characters in text]'
*/

using TMPro;
using System;
using UnityEngine;
using UnityEngine.UI;
using System.Collections;

[Serializable]
public class TemporaryActiveText : TemporaryActiveGameObject
{
	public TMP_Text text;
	public float durationPerCharacter;

	public override void Do ()
	{
		duration = text.text.Length * durationPerCharacter;
		base.Do ();
	}
}