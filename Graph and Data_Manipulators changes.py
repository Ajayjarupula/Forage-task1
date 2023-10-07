#!/usr/bin/env python
# coding: utf-8

# In[ ]:


Graph changes
import React, { Component } from 'react';
import { Table } from '@finos/perspective';
import { ServerRespond } from './DataStreamer';
import './Graph.css';

**()
 * Props declaration for <Graph />
 */
interface IProps {
  data: ServerRespond[],
}

**()
 * Perspective library adds load to HTMLElement prototype.
 * This interface acts as a wrapper for Typescript compiler.
 */
interface PerspectiveViewerElement {
  load: (table: Table) => void,
}

**()
 * React component that renders Perspective based on data
 * parsed from its parent through data property.
 */
class Graph extends Component<IProps, {}> {
  // Perspective table
  table: Table | undefined;

  render() {
    return React.createElement('perspective-viewer');
  }

  componentDidMount() {
    // Get element to attach the table from the DOM.
    const elem: PerspectiveViewerElement = document.getElementsByTagName('perspective-viewer')[0] as unknown as PerspectiveViewerElement;

    const schema = {
      price_abc:'float',
      price_def:'float',
      ratio:'float',
      timestamp:'date',
      upper_bound:'float',
      lower_bound:'float',
      trigger_alert:'float',
    };

    if (window.perspective && window.perspective.worker()) {
      this.table = window.perspective.worker().table(schema);
    }
    if (this.table) {
      // Load the `table` in the `<perspective-viewer>` DOM reference.

      // Add more Perspective configurations here.
      elem.load(this.table);
      elem.setAttribute('view','y_line');
      elem.setAttribute('row-pivots','["timestamp"]');
      elem.setAttribute('columns','["ratio","lower_bound","upper_bound","tigger_alert"]');
      elem.setAttribute('aggregates',JSON.stringify({
          price_abc:'avg',
          price_def:'avg',
          ratio:'avg',
          timestamp:'distinct count',
          upper_bound:'avg',
          lower_bound:'avg',
          trigger_alert:'avg',
      }));     
    }
  }

  componentDidUpdate() {
      if(this.table){
          this.table.update([
              DataManipulator.generateRow(this.props.data),
          ]as unknown as TableData);
    
          stock: el.stock,
          top_ask_price: el.top_ask && el.top_ask.price || 0,
          top_bid_price: el.top_bid && el.top_bid.price || 0,
          timestamp: el.timestamp,
        };
      };
    }
  

export default Graph;


# In[ ]:


DataManipulators change
import { ServerRespond } from './DataStreamer';

export interface Row {
  price_abc:number,
  price_def:number,
  ratio:number,
  timestamp:date,
  upper_bound:number,
  lower_bound:number,
  trigger_alert:number|undefined,
    
}


export class DataManipulator {
  static generateRow(serverResponds: ServerRespond[]) {
      const priceABC=(serverRespond[0].top_ask.price+serverRespond[0].top_bid.price)/2;
      const priceDEF=(serverRespond[1].top_ask.price+serverRespond[1].top_bid.price)/2;
      const ratio=priceABC/priceDEF;
      const upperBound=1+0.05;
      const lowerBound=1-0.05;
      return{
          price_abc:priceABC,
          price_def:priceDEF,
          ratio;
          timestamp:serverRespond[0].timestamp>serverRespond[1].timestamp,
              serverRespond[0].timstamp:serverRespond[1].timestamp,
           upper_bound:upperbound,
           lower_bound:lowerbound,
            trigger_alert:(ratio>upperbound||ratio<lowerbound),ratio:undefined,
      };
    })
  }
}

