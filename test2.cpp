#include <stdio.h>
#include "tester.h"

int main()
{
	rnd.init( 0 );

	CTester< 2 > Tester;
	Tester.init( TestCorpusAll, 0.000001, 500, 2000, false, true );

	Tester.run();
}
