#include "Utils.h"
#include <stdio.h>
#include "Camera/PlayerCameraManager.h"
#include "Templates/SharedPointer.h"
#include "UObject/UObjectGlobals.h"
#include "Prefab.h"
#include "Bullet.h"
#include "UObject/SoftObjectPath.h"
#include <iostream>

Utils::Utils ()
{
	// actor2 = ConstructorHelpers::FObjectFinder<ABullet>(*_assetPath).Object;
}

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

AActor* Utils::SpawnActor (UWorld* world, FString assetPath, FVector location, FRotator rotation)
{
	// FSoftClassPath BlockPath(*assetPath);
	// UClass* blockClass = BlockPath.TryLoadClass<ABullet>();
	// ABullet* actor = LoadObject<ABullet>(nullptr, *assetPath);
	ABullet* actor3 = LoadObject<ABullet>(nullptr, *assetPath);
	// std::cout << std::string{"actor == nullptr"};
	// std::cout << std::endl;
	// if (actor == nullptr)
	// 	std::cout << std::string{"true"};
	// else
	// 	std::cout << std::string{"false"};
	// std::cout << std::endl;
	std::cout << std::string{"actor3 == nullptr"};
	std::cout << std::endl;
	if (actor3 == nullptr)
		std::cout << std::string{"true"};
	else
		std::cout << std::string{"false"};
	// std::cout << std::endl;
	// std::cout << std::string{"blockClass == nullptr"};
	// std::cout << std::endl;
	// if (blockClass == nullptr)
	// 	std::cout << std::string{"true"};
	// else
	// 	std::cout << std::string{"false"};
	// std::cout << std::endl;
	// _assetPath = assetPath;
	// Utils();
	AActor* output = world->SpawnActor(actor3->GetClass(), TSharedPtr<const FVector>(&location).Get(), TSharedPtr<const FRotator>(&rotation).Get(), FActorSpawnParameters());
	// AActor* output = world->SpawnActor(blockClass, TSharedPtr<const FVector>(&location).Get(), TSharedPtr<const FRotator>(&rotation).Get(), FActorSpawnParameters());
	return output;
}

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