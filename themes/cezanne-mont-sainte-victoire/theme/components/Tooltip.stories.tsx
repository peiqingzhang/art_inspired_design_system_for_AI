import type { Meta, StoryObj } from '@storybook/react';
import Tooltip from './Tooltip';

const meta  : Meta<typeof Tooltip> = {
  title: 'Components/Tooltip',
  component: Tooltip,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Tooltip>;

export const Top: Story = { args={{}} };
export const Bottom: Story = { args={{}} };
