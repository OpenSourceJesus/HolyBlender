#include "Utils.h"
#include <stdio.h>
#include "UObject/UObjectGlobals.h"
#include "Kismet/GameplayStatics.h"
#include <iostream>

FVector Utils::GetMousePosition (UWorld* world)
{
	double x;
	double y;
	UGameplayStatics::GetPlayerController(world, 0)->GetMousePosition(x, y);
	return FVector(x, y, 0);
}

FVector Utils::ScreenToWorldPoint (UWorld* world, FVector screenPoint)
{
	FVector output;
	FVector direction;
	UGameplayStatics::DeprojectScreenToWorld(UGameplayStatics::GetPlayerController(world, 0), ToVec2D(screenPoint), output, direction);
	return output;
}

// FVector Utils::GetMousePositionWorld (UWorld* world)
// {
// 	return ScreenToWorldPoint(world, GetMousePosition(world));
// }

FVector2D Utils::ToVec2D (FVector v)
{
	return FVector2D(v.X, v.Y);
}

// AActor Utils::GetActor (FString name, UWorld* world)
// {
// 	for (TActorIterator<AActor> actor(world); actor; ++ actor)
// 	{
// 			return actor;
// 	}
// 	// throw new std::exception();
// 	return nullptr;
// }