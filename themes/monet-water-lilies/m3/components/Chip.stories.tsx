import type { Meta, StoryObj } from '@storybook/react';
import Chip from './Chip';

const meta  : Meta<typeof Chip> = {
  title: 'Components/Chip',
  component: Chip,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Chip>;

export const Default: Story = { args={{ label: 'Chip', selected: false }} };
export const Selected: Story = { args={{ label: 'Chip', selected: true }} };
