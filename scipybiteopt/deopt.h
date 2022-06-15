//$ nocpp

/**
 * @file deopt.h
 *
 * @brief The inclusion file for the CDEOpt class.
 *
 * @section license License
 *
 * Copyright (c) 2021-2022 Aleksey Vaneev
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 *
 * @version 2022.21
 */

#ifndef DEOPT_INCLUDED
#define DEOPT_INCLUDED

#include "biteaux.h"

/**
 * Differential Evolution-alike DFO solver.
 *
 * Description is available at https://github.com/avaneev/biteopt
 */

class CDEOpt : public CBiteOptBase< int64_t >
{
public:
	typedef int64_t ptype; ///< Parameter value storage type (should be a
		///< signed integer type, same as CBiteOptBase template parameter).
		///<

	/**
	 * Function updates dimensionality of *this object.
	 *
	 * @param aParamCount The number of parameters being optimized.
	 * @param PopSize0 The number of elements in population to use. If set to
	 * 0 or negative, the default formula will be used.
	 */

	void updateDims( const int aParamCount, const int PopSize0 = 0 )
	{
		const int aPopSize = ( PopSize0 > 0 ? PopSize0 : 30 * aParamCount );

		if( aParamCount == ParamCount && aPopSize == PopSize )
		{
			return;
		}

		initBuffers( aParamCount, aPopSize );
	}

	/**
	 * Function initializes *this optimizer.
	 *
	 * @param rnd Random number generator.
	 * @param InitParams If not NULL, initial parameter vector, also used as
	 * centroid.
	 * @param InitRadius Initial radius, multiplier relative to the default
	 * sigma value.
	 */

	void init( CBiteRnd& rnd, const double* const InitParams = NULL,
		const double InitRadius = 1.0 )
	{
		getMinValues( MinValues );
		getMaxValues( MaxValues );

		resetCommonVars( rnd );

		const double sd = 0.125 * InitRadius;
		int i;
		int j;

		if( InitParams == NULL )
		{
			for( j = 0; j < PopSize; j++ )
			{
				ptype* const p = PopParams[ j ];

				for( i = 0; i < ParamCount; i++ )
				{
					p[ i ] = wrapParam( rnd, getGaussianInt(
						rnd, sd, IntMantMult >> 1 ));
				}
			}
		}
		else
		{
			ptype* const p0 = PopParams[ 0 ];

			for( i = 0; i < ParamCount; i++ )
			{
				p0[ i ] = wrapParam( rnd,
					(ptype) (( InitParams[ i ] - MinValues[ i ]) /
					DiffValues[ i ]));
			}

			for( j = 1; j < PopSize; j++ )
			{
				ptype* const p = PopParams[ j ];

				for( i = 0; i < ParamCount; i++ )
				{
					p[ i ] = wrapParam( rnd,
						getGaussianInt( rnd, sd, p0[ i ]));
				}
			}
		}

		DoInitEvals = true;
	}

	/**
	 * Function performs the parameter optimization iteration that involves 1
	 * objective function evaluation.
	 *
	 * @param rnd Random number generator.
	 * @param[out] OutCost If not NULL, pointer to variable that receives cost
	 * of the newly-evaluated solution.
	 * @param[out] OutValues If not NULL, pointer to array that receives a
	 * newly-evaluated parameter vector, in real scale, in real value bounds.
	 * @return The number of non-improving iterations so far.
	 */

	int optimize( CBiteRnd& rnd, double* const OutCost = NULL,
		double* const OutValues = NULL )
	{
		int i;

		if( DoInitEvals )
		{
			const ptype* const p = PopParams[ CurPopPos ];

			for( i = 0; i < ParamCount; i++ )
			{
				NewValues[ i ] = getRealValue( p, i );
			}

			const double NewCost = optcost( NewValues );

			if( OutCost != NULL )
			{
				*OutCost = NewCost;
			}

			if( OutValues != NULL )
			{
				copyValues( OutValues, NewValues );
			}

			updateBestCost( NewCost, NewValues,
				updatePop( NewCost, p, false ));

			if( CurPopPos == PopSize )
			{
				DoInitEvals = false;
			}

			return( 0 );
		}

		zeroParams( TmpParams );

		const double r1 = rnd.getSqr();
		const int si1 = (int) ( r1 * r1 * CurPopSize );
		const ptype* const rp1 = getParamsOrdered( si1 );

		const int PairCount = 3;
		const int pc = 1 + 2 * PairCount;
		int PopIdx[ pc ];
		PopIdx[ 0 ] = si1;

		int pp = 1;
		int j;

		if( CurPopSize1 <= pc )
		{
			while( pp < pc )
			{
				PopIdx[ pp ] = rnd.getInt( CurPopSize );
				pp++;
			}
		}
		else
		{
			while( pp < pc )
			{
				const int sii = rnd.getInt( CurPopSize );

				for( j = 0; j < pp; j++ )
				{
					if( PopIdx[ j ] == sii )
					{
						break;
					}
				}

				if( j >= pp )
				{
					PopIdx[ pp ] = sii;
					pp++;
				}
			}
		}

		for( j = 0; j < PairCount; j++ )
		{
			const ptype* const rp2 = getParamsOrdered( PopIdx[ 1 + j * 2 ]);
			const ptype* const rp3 = getParamsOrdered( PopIdx[ 2 + j * 2 ]);

			for( i = 0; i < ParamCount; i++ )
			{
				TmpParams[ i ] += rp2[ i ] - rp3[ i ];
			}
		}

		// TPDF bit randomization.

		if( rnd.getBit() )
		{
			const int k = rnd.getInt( ParamCount );
			const int b = rnd.getInt( IntMantBits );

			TmpParams[ k ] += ( (ptype) rnd.getBit() << b ) -
				( (ptype) rnd.getBit() << b );
		}

		for( i = 0; i < ParamCount; i++ )
		{
			TmpParams[ i ] = rp1[ i ] + ( TmpParams[ i ] >> 2 );
		}

		for( i = 0; i < ParamCount; i++ )
		{
			TmpParams[ i ] = wrapParam( rnd, TmpParams[ i ]);
			NewValues[ i ] = getRealValue( TmpParams, i );
		}

		const double NewCost = optcost( NewValues );

		if( OutCost != NULL )
		{
			*OutCost = NewCost;
		}

		if( OutValues != NULL )
		{
			copyValues( OutValues, NewValues );
		}

		const int p = updatePop( NewCost, TmpParams, false, false );

		if( p < CurPopSize )
		{
			updateBestCost( NewCost, NewValues, p );

			if( PopCosts[ 0 ] == PopCosts[ CurPopSize1 ])
			{
				StallCount++;
			}
			else
			{
				StallCount = 0;
			}
		}
		else
		{
			StallCount++;
		}

		return( StallCount );
	}

protected:
	bool DoInitEvals; ///< "True" if initial evaluations should be performed.
		///<
};

#endif // DEOPT_INCLUDED
