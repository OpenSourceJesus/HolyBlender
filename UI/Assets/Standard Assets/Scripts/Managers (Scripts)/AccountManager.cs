using UnityEngine;
using System;

namespace HolyBlender
{
	public class AccountManager : SingletonMonoBehaviour<AccountManager>, ISaveableAndLoadable
	{
		public static Account CurrentAccount
		{
			get
			{
				return Instance.accounts[currentAccountIndex];
			}
			set
			{
				Instance.accounts[currentAccountIndex] = value;
			}
		}
		public static int currentAccountIndex;
		[SaveAndLoadValue]
		public Account[] accounts = new Account[0];

		[Serializable]
		public class Account
		{
			public string name;
			public string password;
			public uint score;
			public uint masteryScore;
			public uint masteryHighscore;
		}
	}
}